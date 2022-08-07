import pytest
import json
import os

from market.binance_market import BinanceMarketConnector

@pytest.fixture
def binance():
    key_path = os.path.join('config','key.json')
    with open(key_path) as f:
        key = json.load(f)
    bmc = BinanceMarketConnector(key['BINANCE'])

    return bmc

def test_get_balance(binance):
    binance.get_balance()

def test_get_unify_balance(binance):
    res = binance.get_unify_balance()
    assert res > 10