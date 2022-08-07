class MarketInterface():

    def __init__(self, Token):
        self.__balance = self.get_balance()

    def login(self, Token):
        raise NotImplementedError('users must define get_balance to use this base class')

    def get_balance(self):
        raise NotImplementedError('users must define get_balance to use this base class')

    def open_order_execute(self, symbol, price, volume, side):
        raise NotImplementedError('users must define open_order_execute to use this base class')

    def open_order(self,
        symbol, # required: BTC/BUSD, XRP/BTC etc
        price,  # not required
        volume, # required
        trade_side, # required: BUY / SELL

    ):
        raise  NotImplementedError('users must define open_order to use this base class')

    def get_symbols(self):
        raise NotImplementedError('users must define get_symbols to use this base class')

    def get_order_book(self, symbol):
        raise NotImplementedError('users must define get_symbols to use this base class')

    def cancel_all_order(self, symbol):
        raise NotImplementedError('users must define get_symbols to use this base class')

    def get_symbol_detail(self, symbol):
        raise NotImplementedError('users must define get_symbols to use this base class')