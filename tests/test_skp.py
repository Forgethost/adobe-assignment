import pytest
from src.lambdas.search_keyword_performance.app import *


@pytest.fixture (autouse=True)
def skp_object ():
    skp_obj = SearchKeywordPerformance(
    None,
    None,
    "www.esshopzilla.com",
    "https:/www.esshopzilla. com/checkout/?a=complete"
    )
    return skp_obj


def test_parse_product_ist (skp_object):
    assert skp_object. _parse_product_list("a;b;c;12;200|300,a;b;c;10;200|300") == 22.00
    assert skp_object. _parse_product_list ("Electronics;Ipod - Nano - 8GB;1;190;") == 190.00


def test_parse_referrer(skp_object):
    assert skp_object._parse_referrer(
    "http://www.google.com/search?hl=en&client=firefox-a&rls=org.mozilla%3Aen-US%3Aofficial&hs=ZzP&q=Ipod&aq=f&oq=&aqi="
    ) == "google.com"

    assert skp_object. _parse_referrer(
    "http://www.bing.com/search?q=Zune&go=&form=QBLH&qs=n") == "bing.com"

    assert skp_object._parse_referrer(
    "http://search.yahoo.com/search?p=cd+player&toggle=1&cop=mss&ei=UTF-8&fr=yfp-t-701"
    ) == "yahoo.com"


def test_parse_search_str(skp_object):
    assert skp_object._parse_search_str(
    "http://www.google.com/search?hl=en&client=firefox-a&rls=org.mozilla%3Aen-US%3Aofficial&hs=ZzP&q=Ipod&aq=f&oq=&aqi="
    ) == "Ipod"

    assert skp_object._parse_search_str(
    "http://www.bing.com/search?q=Zune&go=&form=QBLH&qs=n") == "Zune"

    assert skp_object._parse_search_str(
    "http://search.yahoo.com/search?p=cd+player&toggle=1&cop=mss&ei=UTF-8&fr=yfp-t-701"
    ) == "cd"