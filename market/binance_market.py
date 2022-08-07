from market.market_interface import MarketInterface
from binance.client import Client
from binance.enums import *

DEFAULT_CURRENCY_LIST = ['BUSD', 'USDT']

class BinanceMarketConnector(MarketInterface):

    def __init__(self, token, default_currency = 'BUSD'):
        self.default_currency = default_currency
        self.login(token['API_KEY'], token['API_SECRET'])

    def login(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)

    def get_balance(self, default_currency = None):
        if default_currency is None:
            default_currency = self.default_currency
        info = self.client.get_account()
        balances = info.get('balances', [])
        balances = [_ for _ in balances if float(_.get('free')) > 0.0001]

        def bn_info_to_sys_info(bn_info):
            del bn_info['locked']
            bn_info['free'] = float(bn_info.get('free', 0))
            if bn_info.get('asset') in DEFAULT_CURRENCY_LIST:
                bn_info['value'] = bn_info['free']
            else:
                price = self.get_symbol_price(f"{bn_info['asset']}{default_currency}")
                bn_info['value'] = bn_info['free'] * price
            return bn_info

        balances = [bn_info_to_sys_info(_) for _ in balances]
        balances = [_ for _ in balances if _['value'] > 10]

        return balances

    def get_symbol_price(self, symbol):
        symbol = f"{symbol}"
        trade_info = self.client.get_recent_trades(symbol=symbol, limit=1)
        return float(trade_info[0]['price'])

    def get_unify_balance(self, default_currency = None):
        res = self.get_balance(default_currency=default_currency)
        values = [_['value'] for _ in res ]
        return sum(values)

    def refine_order_volume(self, symbol, volume):
        step_size = self.get_step_size(symbol)

        volume /= volume / step_size
        volume //= volume // 1
        volume *= volume * step_size

        return volume

    def open_order(self,
        symbol, # required: BTC/BUSD, XRP/BTC etc
        side,  # required: BUY / SELL
        volume,  # required
        price,  # None => Semi Market Price (order book [10])
    ):
        if price is None:
            order_book = self.get_order_book(symbol, limit=10)
            price = order_book[side][-1]
        volume = self.refine_order_volume(symbol, volume)

        side = SIDE_BUY if side == "BUY" else SIDE_SELL

        self.client.create_order(
            symbol=symbol,
            side=side,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=volume,
            price=price
        )

    def get_symbols(self):
        print("get_symbols")

    def get_order_book(self, symbol, limit=10):
        res = self.client.get_order_book(symbol=symbol, limit=limit)
        res = {
            "SELL": [float(_[0]) for _ in res["asks"] ],
            "BUY": [float(_[0]) for _ in res["bids"] ]
        }
        return res

    def cancel_all_order(self, symbol):
        print("cancel_all_order")

    def get_symbol_detail(self, symbol):
        info = self.client.get_symbol_info(symbol)
        return info

    def get_step_size(self, symbol):
        info = self.get_symbol_detail(symbol)
        filters = info['filters']
        lot_size = [_ for _ in filters if _['filterType'] == 'LOT_SIZE'][0]

        return float(lot_size['stepSize'])