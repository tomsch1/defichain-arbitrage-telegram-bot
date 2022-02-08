import json

import requests

import dex_ticker
from symbols import CryptoExchangeSymbols, StockTokenSymbols


class DfiDexPrices():

    def __init__(self):
        self.d_tokens = {CryptoExchangeSymbols.DFIBTC.d_token(): 5,
                         CryptoExchangeSymbols.DFIETH.d_token(): 4,
                         CryptoExchangeSymbols.DFIUSDT.d_token(): 6,
                         CryptoExchangeSymbols.DFILTC.d_token(): 10,
                         CryptoExchangeSymbols.DFIUSDC.d_token(): 14,
                         CryptoExchangeSymbols.DFIBCH.d_token(): 12,
                         CryptoExchangeSymbols.DFIDOGE.d_token(): 8
                         }
        self.stock_token = StockTokenSymbols.dict()
        self.api_url = "https://ocean.defichain.com/v0/mainnet/poolpairs/"
        self.update_dex_crypto_tickers()
        self.update_dex_stock_tickers()

    dex_crypto_state_map = {}
    dex_stock_token_state_map = {}




    def get_dex_price(self, token_id):
        r = requests.get(self.api_url + str(token_id))
        return dex_ticker.dex_ticker_from_dict(json.loads(r.content))

    def update_dex_crypto_tickers(self) -> None:
        pair_dict = {}
        for symbol, id in self.d_tokens.items():
            dex_ticker = self.get_dex_price(id)
            pair_dict[symbol] = dex_ticker
        self.dex_crypto_state_map = pair_dict

    def update_dex_stock_tickers(self) -> None:
        pair_dict = {}
        for symbol, id in self.stock_token.items():
            dex_ticker = self.get_dex_price(id)
            pair_dict[symbol] = dex_ticker
        self.dex_stock_token_state_map = pair_dict
