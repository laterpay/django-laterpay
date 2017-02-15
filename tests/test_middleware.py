# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function


from django.conf import settings
# Configure settings before attempting to import modules depending on them.
settings.configure(
    ALLOWED_HOSTS=["*"],
    LP_CONTENT_PROVIDER_KEY='merchant-key',
    LP_SECRET='merchant-super-secret',
    LP_API_ROOT='https://web.sandbox.laterpaytest.net',
)

from django.test import RequestFactory, SimpleTestCase
from django.utils import six

from laterpay import signing

from djlaterpay.middleware import LPTokenMiddleware


class MiddlewareTest(SimpleTestCase):

    def setUp(self):
        self.request_factory = RequestFactory()

    def test_exempt_paths(self):
        paths = ('/one', '/two')
        LPTokenMiddleware.add_exempt_paths(*paths)

        for path in paths:
            request = self.request_factory.get(path)
            m = LPTokenMiddleware()
            self.assertEqual(m.process_request(request), None)

    def _test_lptoken_validation(self, data, method=None, cookie_token=False):
        request_factory_method = method or self.request_factory.get
        request = request_factory_method('/end', data)
        if cookie_token:
            request.COOKIES['__lptoken'] = 'tokentoken'
        middleware = LPTokenMiddleware()
        response = middleware.process_request(request)
        return (request, response)

    def test_lptoken_validation_from_cookie(self):
        request, response = self._test_lptoken_validation({}, cookie_token=True)
        self.assertEqual(request.laterpay.lptoken, 'tokentoken')

    def test_lptoken_validation_no_token(self):
        request, response = self._test_lptoken_validation({})
        redirect_location = response['Location']
        query = six.moves.urllib.parse.urlparse(redirect_location).query
        params = six.moves.urllib.parse.parse_qs(query)
        verified = signing.verify(
            signature=params['hmac'],
            secret=settings.LP_SECRET,
            params=params,
            url=settings.LP_API_ROOT + '/gettoken',
            method='GET',
        )
        self.assertTrue(verified)

    def test_lptoken_validation_no_token_on_post(self):
        request, response = self._test_lptoken_validation(
            {},
            method=self.request_factory.post,
        )
        # We don't do anything with the request except for setting
        # request.laterpay.lptoken to None
        self.assertEqual(request.laterpay.lptoken, None)

    def test_lptoken_validation_no_hmac(self):
        request, response = self._test_lptoken_validation({
            'lptoken': 'tokentoken',
            'ts': '141500500',
        })
        self.assertEqual(request.laterpay.lptoken, None)

    def test_lptoken_validation_no_timestamp(self):
        request, response = self._test_lptoken_validation({
            'lptoken': 'tokentoken',
            'hmac': 'a-fake-signature',
        })
        self.assertEqual(request.laterpay.lptoken, None)

    def test_lptoken_validation_wrong_signature(self):
        params = {
            'lptoken': 'tokentoken',
            'ts': '141500500',
        }
        signature = 'wrong'

        data = params.copy()
        data['hmac'] = signature

        request, response = self._test_lptoken_validation(data)

        self.assertEqual(request.laterpay.lptoken, None)

    def test_lptoken_validation_ok(self):
        params = {
            'lptoken': 'tokentoken',
            'ts': '141500500',
        }
        signature = signing.sign(
            secret='merchant-super-secret',
            params=params,
            url='http://testserver/end',
            method='GET',
        )
        data = params.copy()
        data['hmac'] = signature

        request, response = self._test_lptoken_validation(data)

        self.assertEqual(request.laterpay.lptoken, 'tokentoken')
