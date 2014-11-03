import re
from django.template import Library
import warnings

warnings.warn("""djlaterpay.templatetags.laterpay is deprecated; it is
undocumented and, to the best of our knowledge, unused outside of some (also
deprecated) internal cases. If you _are_ using it, please contact us via
https://github.com/laterpay/django-laterpay - otherwise, it will be removed in
the next major release.""", DeprecationWarning)

register = Library()


def render_laterpay_header(context):
    laterpay = context['request'].laterpay

    # strip the protocol
    web_root = re.sub('^https?://', '', laterpay.web_root)

    return {'web_root': web_root}

register.inclusion_tag('laterpay/inclusion/render_header.html', takes_context=True)(render_laterpay_header)


def render_laterpay_footer(context, identify_callback=None):
    if identify_callback == '':
        identify_callback = None
    laterpay = context['request'].laterpay
    return {'identify_url': laterpay.get_identify_url(identify_callback)}

register.inclusion_tag('laterpay/inclusion/render_footer.html', takes_context=True)(render_laterpay_footer)


def laterpay_subscribe(context, product_key=None, subscription_key=None):
    laterpay = context['request'].laterpay
    return laterpay.get_subscription_url(product_key, subscription_key)

register.simple_tag(takes_context=True)(laterpay_subscribe)


def laterpay_buy(context, item_definition, product_key=None):
    laterpay = context['request'].laterpay
    return laterpay.get_buy_url(item_definition, product_key)

register.simple_tag(takes_context=True)(laterpay_buy)
