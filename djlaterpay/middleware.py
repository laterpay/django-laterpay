import logging

from django.conf import settings
from django.http import HttpResponseRedirect

from laterpay import signing

from djlaterpay import get_laterpay_client

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    # TODO Remove when dropping Django 1.8
    MiddlewareMixin = object


_logger = logging.getLogger(__name__)


LPTOKEN_COOKIENAME = getattr(settings, 'LPTOKEN_COOKIENAME', '__lptoken')


class LPTokenMiddleware(MiddlewareMixin):

    exempt_paths = []

    @classmethod
    def add_exempt_paths(cls, *paths):
        """
        Exempts given ``paths`` from processing by ``LPTokenMiddleware``.
        """
        cls.exempt_paths.extend(paths)

    def process_request(self, request):
        """
        Pulls the LPToken out of our cookie if we have set
        it, and adds it to the request object for easy access
        during views.
        """
        if request.path in self.exempt_paths:
            return

        verified_lptoken = None
        lptoken_param = request.GET.get('lptoken', None)
        absolute_url = request.build_absolute_uri()

        if lptoken_param is None:
            if LPTOKEN_COOKIENAME in request.COOKIES:
                # we have a token already, carry on
                verified_lptoken = request.COOKIES[LPTOKEN_COOKIENAME]
            else:
                # we don't have a cookie, so we need to go to /identify to get one
                # first figure out where we are, so we can get back
                if request.method == 'GET':
                    here = request.build_absolute_uri()
                    return HttpResponseRedirect(
                        get_laterpay_client(None).get_gettoken_redirect(return_to=here)
                    )
                # Don't do anything on POST and such
        else:
            # Validate lptoken's signature.
            base_url = absolute_url.split('?')[0]
            signature = request.GET.get('hmac')
            timestamp = request.GET.get('ts')

            if None in (signature, timestamp):
                _logger.warning(
                    'Received lptoken without signature and/or timestamp: %s',
                    absolute_url,
                )
            else:
                data = {
                    'lptoken': lptoken_param,
                    'ts': timestamp,
                }

                verified = signing.verify(
                    signature=signature,
                    secret=settings.LP_SECRET,
                    params=data,
                    url=base_url,
                    method=request.method,
                )

                if verified:
                    verified_lptoken = lptoken_param
                else:
                    _logger.warning(
                        'Received lptoken with invalid signature: %s',
                        absolute_url,
                    )

        if verified_lptoken is None:
            _logger.info(
                'Setting ``request.laterpay.lptoken`` to ``None`` for %s %s',
                request.method,
                absolute_url,
            )

        request.laterpay = get_laterpay_client(verified_lptoken)

    def process_response(self, request, response):
        """
        If the LPToken has been added to the request
        object, set the cookie on the response to ensure
        we get it next request.
        """
        if not hasattr(request, 'laterpay'):
            # this means that some other middleware returned from process_request
            # before ours was run - for example, the django middleware which adds
            # a trailing slash to URLs will do this
            return response

        if request.laterpay.lptoken:
            response.set_cookie(LPTOKEN_COOKIENAME, request.laterpay.lptoken)
        else:
            response.delete_cookie(LPTOKEN_COOKIENAME)
            here = request.build_absolute_uri()
            return HttpResponseRedirect(
                request.laterpay.get_gettoken_redirect(return_to=here)
            )
        return response
