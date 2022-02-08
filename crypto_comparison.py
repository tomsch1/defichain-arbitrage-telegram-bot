import cexdatacollect
import dfi_dex_prices
from symbols import CryptoExchangeSymbols


class SymbolPrice():
    def __init__(self, exchange_name:str, symbol:str, price:float):
        self.exchange_name: str = exchange_name
        self.symbol: str = symbol
        self.price: float = price

class IndirectComparison():
    def __init__(self, ex_name: str, cex_dfi_pair: SymbolPrice, dex_dfi_pair: SymbolPrice, intermediate_pair: SymbolPrice=None, percentage_minus_one :bool = True):
        self.ex_name: str = ex_name
        self.dex_dfi_pair = dex_dfi_pair
        self.cex_dfi_pair = cex_dfi_pair
        self.intermediate_pair = intermediate_pair
        if intermediate_pair is None:
            perc = (dex_dfi_pair.price/cex_dfi_pair.price)
            if percentage_minus_one:
                perc = perc -1
            self.percentage: float = perc
        else:
            print(f"{dex_dfi_pair.symbol} = {dex_dfi_pair.price}, {intermediate_pair.symbol} = {intermediate_pair.price}, {cex_dfi_pair.symbol} = {cex_dfi_pair.price}")
            perc = (dex_dfi_pair.price/(cex_dfi_pair.price/intermediate_pair.price))
            if percentage_minus_one:
                perc = perc -1
            self.percentage: float = perc

class AggregatedComparison():

    def __init__(self, cex_name: str, symbol, cex_price, dex_price):
        self.cex_name: str = cex_name
        self.symbol: CryptoExchangeSymbols = symbol
        self.cex_price: float = cex_price
        self.dex_price: float = dex_price
        self.percentage: float = (dex_price/cex_price)-1



class CryptoComparison():



    all_pairs = []

    def __init__(self, dex_data: dfi_dex_prices.DfiDexPrices, cex_data: cexdatacollect.CexPriceFetch):
        self.dex_data = dex_data
        self.cex_data = cex_data


    def get_indirect_comparison(self, dfi_symbol: CryptoExchangeSymbols, intermediate_symbol: CryptoExchangeSymbols = None, inverse_intermediate_symbol: bool = False, inverse_cex_dfi_price: bool = True):
        exchange_name = 'KuCoin'
        dex_dfi_price = float(self.dex_data.dex_crypto_state_map[dfi_symbol.d_token()].data.price_ratio.ba)
        if intermediate_symbol is not None:
            intermediate_price = 1/float(self.cex_data.cex_price_state[exchange_name][intermediate_symbol.value]['last'])
            if inverse_intermediate_symbol:
                new_cex_symbol = f"DFI/{intermediate_symbol.value.split('/')[0]}"
                inverse_intermediate_symbol = f"{intermediate_symbol.value.split('/')[1]}/{intermediate_symbol.value.split('/')[0]}"
                intermediate_pair = SymbolPrice(exchange_name, inverse_intermediate_symbol, intermediate_price)
            else:
                new_cex_symbol = f"DFI/{intermediate_symbol.value.split('/')[1]}"
                intermediate_pair = SymbolPrice(exchange_name, intermediate_symbol.value, intermediate_price)
            cex_dfi_price = float(self.cex_data.cex_price_state[exchange_name][new_cex_symbol]['last'])
            if inverse_cex_dfi_price:
                cex_dfi_price = 1 / cex_dfi_price
            cex_dfi_pair = SymbolPrice(exchange_name, new_cex_symbol, cex_dfi_price)
        else:
            intermediate_pair = None
            cex_dfi_price = float(self.cex_data.cex_price_state[exchange_name][dfi_symbol.value]['last'])
            if inverse_cex_dfi_price:
                cex_dfi_price = 1 / cex_dfi_price
            cex_dfi_pair = SymbolPrice(exchange_name, dfi_symbol.value, cex_dfi_price)
        return IndirectComparison(
            ex_name=exchange_name,
            cex_dfi_pair=cex_dfi_pair,
            dex_dfi_pair=SymbolPrice('dex', dfi_symbol.value, dex_dfi_price),
            intermediate_pair=intermediate_pair,
            percentage_minus_one=inverse_cex_dfi_price
        )

    def get_all_comparisons(self) -> [SymbolPrice]:
        return [
            self.get_indirect_comparison(CryptoExchangeSymbols.DFIBTC, None),
            self.get_indirect_comparison(CryptoExchangeSymbols.DFIUSDT, None),
            self.get_maximum_percentage(CryptoExchangeSymbols.DFIETH, [CryptoExchangeSymbols.ETHBTC, CryptoExchangeSymbols.ETHUSDT]),
            self.get_maximum_percentage(CryptoExchangeSymbols.DFILTC, [CryptoExchangeSymbols.LTCBTC, CryptoExchangeSymbols.LTCUSDT]),
            #Something is wrong here!
            #self.get_indirect_comparison(ExchangeSymbol.DFIUSDC, ExchangeSymbol.BTCUSDC, True, False),
            self.get_indirect_comparison(CryptoExchangeSymbols.DFIUSDC, CryptoExchangeSymbols.USDTUSDC, True),
            self.get_maximum_percentage(CryptoExchangeSymbols.DFIBCH, [CryptoExchangeSymbols.BCHBTC, CryptoExchangeSymbols.BCHUSDT]),
            self.get_maximum_percentage(CryptoExchangeSymbols.DFIDOGE, [CryptoExchangeSymbols.DOGEBTC, CryptoExchangeSymbols.DOGEUSDT]),
        ]

    def get_maximum_percentage(self, dfi_symbol: CryptoExchangeSymbols, intermediate_pairs: [CryptoExchangeSymbols]):
        all_paths = []
        percentages = []
        for pair in intermediate_pairs:
            path = self.get_indirect_comparison(dfi_symbol, pair)
            all_paths.append(path)
            percentages.append(abs(path.percentage))
        index_of_highest_percentage =  percentages.index(max(percentages))
        return all_paths[index_of_highest_percentage]


    def update_pairs(self):
        self.all_pairs = self.get_all_comparisons()






    def get_overview(self):
        pairs: [SymbolPrice] = self.get_all_comparisons()
        pair_text = []
        for pair in sorted(pairs, key=lambda x: abs(x.percentage), reverse=True):
            if pair.intermediate_pair is None:
                text = f"""
                DFI -> {pair.dex_dfi_pair.symbol.split('/')[1]}:
                DEX:\t{round(pair.dex_dfi_pair.price, 3)} DFI
                {pair.ex_name}:\t{round(pair.cex_dfi_pair.price, 3)} DFI
                \t{round(pair.percentage*100, 2)} %
                """
            else:
                text = f"""
                DFI -> {pair.dex_dfi_pair.symbol.split('/')[1]}:
                DEX:\t{round(pair.dex_dfi_pair.price, 3)} DFI
                {pair.ex_name} via {pair.intermediate_pair.symbol.split('/')[1]}:\t{round(pair.cex_dfi_pair.price / pair.intermediate_pair.price, 3)} DFI
                \t{round(pair.percentage * 100, 2)} %
                """
            pair_text.append(text)
        single_pair_text_string = '\n'.join(pair_text)
        return f" Current premium overview:\n{single_pair_text_string}"


    def evaluate_alarm(self, symbol_name, threshold: float):
        for pair in self.all_pairs:
            symbol = CryptoExchangeSymbols.from_string(symbol_name)
            if pair.dex_dfi_pair.symbol == symbol.value:
                if abs(pair.percentage) >= abs(threshold):
                    return pair





