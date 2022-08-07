from market.market_interface import MarketInterface
from binance.client import Client

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
        res = self.get_balance()
        values = [_["value"] for _ in res ]
        return sum(values)

    def open_order_execute(self, symbol, price, volume, side):
        print("open_order_execute")

    def open_order(self,
        symbol, # required: BTC/BUSD, XRP/BTC etc
        price,  # not required
        volume, # required
        trade_side, # required: BUY / SELL

    ):
        print("open_order")

    def get_symbols(self):
        print("get_symbols")

    def get_order_book(self, symbol):
        print("get_order_book")

    def cancel_all_order(self, symbol):
        print("cancel_all_order")

    def get_symbol_detail(self, symbol):
        print("get_symbol_detail")