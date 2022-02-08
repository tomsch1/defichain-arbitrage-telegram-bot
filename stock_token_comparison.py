import dfi_dex_prices
import dfi_oracle_prices
import symbols
from symbols import StockTokenSymbols


class PairComparison():

    def __init__(self, symbol, oracle_price, dex_price):
        self.symbol: StockTokenSymbols = symbol
        self.oracle_price: float = oracle_price
        self.dex_price: float = dex_price
        self.percentage: float = (dex_price/oracle_price)-1



class StockComparison():

    pair_list = []


    def __init__(self, dfi_dex_data: dfi_dex_prices.DfiDexPrices, dfi_oracle_data: dfi_oracle_prices.DfiOraclePrices):
        self.dex_data = dfi_dex_data
        self.oracle_data = dfi_oracle_data


    def update_data(self):
        self.dex_data.update_dex_stock_tickers()
        self.oracle_data.update_dfi_oracle_stock_tickers()
        self.pair_list = self.compare_all()



    def compare_pair(self, symbol: symbols.StockTokenSymbols):
        dex_data = self.dex_data.dex_stock_token_state_map[symbol.name]
        oracle_data = self.oracle_data.dfi_oracle_stock_token_state_map[symbol.name]
        if 'DFI' in symbol.name:
            return PairComparison(symbol, float(oracle_data.data.price.aggregated.amount),
                                  float(dex_data.data.price_ratio.ab))
        else:
            return PairComparison(symbol, float(oracle_data.data.price.aggregated.amount), float(dex_data.data.price_ratio.ba))


    def compare_all(self):
        all_pairs = []
        for i in symbols.StockTokenSymbols.list():
            all_pairs.append(self.compare_pair(i))
        #for i in all_pairs:
            #print(f"{i.symbol}, oracle price ={i.oracle_price}, dex price = {i.dex_price}, dex premium = {i.percentage*100}")
        return all_pairs



    def get_overview(self):
        pairs = self.compare_all()
        pair_text = []
        for pair in sorted(pairs, key=lambda x: abs(x.percentage), reverse=True):
            if not 'DFI' in pair.symbol.name:
                text = f"""
                {pair.symbol.name.replace('DUSD', '-DUSD')}:
                DEX:\t{round(pair.dex_price, 3)} DUSD
                Oracle:\t{round(pair.oracle_price, 3)} USD
                \t{round(pair.percentage*100, 2)} %
                """
            else:
                text = f"""
                DUSD-DFI:
                DEX:\t{round(pair.dex_price, 3)} DUSD
                Oracle:\t{round(pair.oracle_price, 3)} USD
                \t{round(pair.percentage*100, 2)} %
                """
            pair_text.append(text)
        single_pair_text_string = '\n'.join(pair_text)
        return f" Current premium overview:\n{single_pair_text_string}"


    def evaluate_alarm(self, symbol_name, threshold: float):
        for pair in self.pair_list:
            symbol = StockTokenSymbols.from_string(symbol_name)
            if pair.symbol == symbol:
                if pair.percentage >= threshold:
                    return pair

