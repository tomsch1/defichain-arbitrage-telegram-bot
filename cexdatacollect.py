import json



import ccxt

from cex_ticker import cex_ticker_from_dict
from symbols import CryptoExchangeSymbols


class CexPriceFetch():


    cex = [ccxt.ftx(), ccxt.kucoin()]
    tickers = CryptoExchangeSymbols.list()
    supported_symbols = {}
    cex_price_state = {}

    def __init__(self):
        for exchange in self.cex:
            markets = exchange.fetch_markets()
            symbols = [d['symbol'] for d in markets if 'symbol' in d]
            self.supported_symbols[exchange.name] = symbols
        self.update_all_tickers()





    def get_single_ticker(self, exchange: ccxt.Exchange, ticker):
        if exchange.has['fetchTicker']:
            if ticker in self.supported_symbols[exchange.name]:
                return exchange.fetch_ticker(ticker)

    def get_all_tickers_of_exchange(self, exchange: ccxt.Exchange):
        ticker_feeds = {}
        symbols = [symbol for symbol in self.tickers if symbol not in self.supported_symbols]
        ticker_feeds = exchange.fetch_tickers(symbols)
        return ticker_feeds

    def update_all_tickers(self) -> None:
        exchange_feed = {}
        for exchange in self.cex:
            all_tickers = self.get_all_tickers_of_exchange(exchange)
            exchange_feed[exchange.name] = all_tickers
        self.cex_price_state = exchange_feed




