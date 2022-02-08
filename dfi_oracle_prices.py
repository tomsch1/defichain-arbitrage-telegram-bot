import json

import requests

import dex_ticker
import dfi_oracle_ticker
from symbols import CryptoExchangeSymbols, StockTokenSymbols


class DfiOraclePrices():

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
        self.api_url = "https://ocean.defichain.com/v0/mainnet/prices/"
        self.update_dfi_oracle_crypto_tickers()
        self.update_dfi_oracle_stock_tickers()

    dfi_oracle_crypto_state_map = {}
    dfi_oracle_stock_token_state_map = {}


    def print_dfi_oracle_price_map(self, ticker_list:  {dfi_oracle_ticker.DfiOracleTicker}):
        for symbol, item in ticker_list.items():
            if item is not None:
                price = item.data.price.aggregated.amount
                print(f'{symbol} = {price} USD')




    def get_dex_price(self, token_symbol):
        r = requests.get(self.api_url + str(token_symbol))
        return dfi_oracle_ticker.dfi_oracle_ticker_from_dict(json.loads(r.content))

    def update_dfi_oracle_crypto_tickers(self) -> None:
        pair_dict = {}
        for symbol, id in self.d_tokens.items():
            oracle_symbol = symbol.split('-')[0]
            dex_ticker = self.get_dex_price(f'{oracle_symbol}-USD')
            pair_dict[symbol] = dex_ticker
        self.dfi_oracle_crypto_state_map = pair_dict
        #print(self.print_dfi_oracle_price_map(self.dfi_oracle_crypto_state_map))

    def update_dfi_oracle_stock_tickers(self) -> None:
        pair_dict = {}
        for symbol, id in self.stock_token.items():
            oracle_symbol = symbol.replace('DUSD', '')
            dex_ticker = self.get_dex_price(f'{oracle_symbol}-USD')
            pair_dict[symbol] = dex_ticker
        self.dfi_oracle_stock_token_state_map = pair_dict
        #print(self.print_dfi_oracle_price_map(self.dfi_oracle_stock_token_state_map))
