# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import unittest

from django.conf import settings
# Configure settings before attempting to import modules depending on them.
settings.configure(
    ALLOWED_HOSTS=["*"],
    LP_CONTENT_PROVIDER_KEY='merchant-key',
    LP_SECRET='merchant-super-secret',
)

from django.test.client import RequestFactory

from laterpay import signing

from djlaterpay.middleware import LPTokenMiddleware


class RequestMock:

    def __init__(self, path):
        self.path = path


class MiddlewareTest(unittest.TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()

    def test_exempt_paths(self):
        paths = ('/one', '/two')
        LPTokenMiddleware.add_exempt_paths(*paths)

        for path in paths:
            request = RequestMock(path)
            m = LPTokenMiddleware()
            self.assertEqual(m.process_request(request), None)

    def _test_lptoken_validation(self, data):
        request = self.request_factory.get('/end', data)
        middleware = LPTokenMiddleware()
        middleware.process_request(request)
        return request

    def test_lptoken_validation_no_hmac(self):
        request = self._test_lptoken_validation({
            'lptoken': 'tokentoken',
            'ts': '141500500',
        })
        self.assertEqual(request.laterpay.lptoken, None)

    def test_lptoken_validation_no_timestamp(self):
        request = self._test_lptoken_validation({
            'lptoken': 'tokentoken',
            'hmac': 'a-fake-signature',
        })
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

        request = self._test_lptoken_validation(data)

        self.assertEqual(request.laterpay.lptoken, 'tokentoken')
