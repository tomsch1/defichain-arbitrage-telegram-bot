from enum import Enum



class CryptoExchangeSymbols(Enum):
    DFIBTC ='DFI/BTC'
    DFIUSDT='DFI/USDT'
    DFIETH='DFI/ETH'
    DFILTC='DFI/LTC'
    DFIUSDC='DFI/USDC'
    DFIBCH='DFI/BCH'
    DFIDOGE='DFI/DOGE'
    ETHBTC='ETH/BTC'
    ETHUSDT='ETH/USDT'
    LTCBTC='LTC/BTC'
    LTCUSDT='LTC/USDT'
    BTCUSDC='BTC/USDC'
    USDTUSDC='USDT/USDC'
    BCHBTC='BCH/BTC'
    BCHUSDT='BCH/USDT'
    DOGEBTC='DOGE/BTC'
    DOGEUSDT='DOGE/USDT'
    BTCUSD='BTC/USD'
    ETHUSD='ETH/USD'
    USDTUSD='USDT/USD'
    LTCUSD='LTC/USD'
    BCHUSD='BCH/USD'
    DOGEUSD='DOGE/USD'

    def d_token(self):
        if 'DFI' not in self.value:
            print(f"Symbol {self} does not contain DFI")
            return
        not_dfi_part = self.value.split('/')[1]
        return f"{not_dfi_part}-DFI"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def name_list(cls):
        return [i.name for i in CryptoExchangeSymbols]

    @classmethod
    def from_string(cls, token_string: str):
        for i in CryptoExchangeSymbols:
            if i.name == token_string:
                return i


class StockTokenSymbols(Enum):
    DUSDDFI = 17
    TSLADUSD = 18
    GMEDUSD = 25
    BABADUSD = 33
    GOOGLDUSD = 32
    AAPLDUSD = 36
    PLTRDUSD = 35
    ARKKDUSD = 42
    SPYDUSD = 38
    QQQDUSD = 39
    GLDDUSD = 43
    SLVDUSD = 46
    PDBCDUSD = 40
    VNQDUSD = 41
    URTHDUSD = 44
    TLTDUSD = 45
    NVDADUSD = 55
    COINDUSD = 56
    AMZNDUSD = 54
    EEMDUSD = 53

    @classmethod
    def dict(cls):
        return {i.name: i.value for i in StockTokenSymbols}

    @classmethod
    def list(cls):
        return [i for i in StockTokenSymbols]

    @classmethod
    def name_list(cls):
        return [i.name for i in StockTokenSymbols]

    @classmethod
    def from_string(cls, token_string: str):
        for i in StockTokenSymbols:
            if i.name == token_string:
                return i