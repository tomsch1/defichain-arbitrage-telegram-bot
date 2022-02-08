# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = cex_ticker_from_dict(json.loads(json_string))

from typing import Any, TypeVar, Type, cast
from datetime import datetime
import dateutil.parser


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Info:
    ask: str
    base_currency: str
    bid: str
    change1_h: str
    change24_h: str
    change_bod: str
    enabled: str
    high_leverage_fee_exempt: str
    last: str
    min_provide_size: str
    name: str
    post_only: str
    price: str
    price_increment: str
    quote_currency: str
    quote_volume24_h: str
    restricted: str
    size_increment: str
    type: str
    volume_usd24_h: str

    def __init__(self, ask: str, base_currency: str, bid: str, change1_h: str, change24_h: str, change_bod: str, enabled: str, high_leverage_fee_exempt: str, last: str, min_provide_size: str, name: str, post_only: str, price: str, price_increment: str, quote_currency: str, quote_volume24_h: str, restricted: str, size_increment: str, type: str, volume_usd24_h: str) -> None:
        self.ask = ask
        self.base_currency = base_currency
        self.bid = bid
        self.change1_h = change1_h
        self.change24_h = change24_h
        self.change_bod = change_bod
        self.enabled = enabled
        self.high_leverage_fee_exempt = high_leverage_fee_exempt
        self.last = last
        self.min_provide_size = min_provide_size
        self.name = name
        self.post_only = post_only
        self.price = price
        self.price_increment = price_increment
        self.quote_currency = quote_currency
        self.quote_volume24_h = quote_volume24_h
        self.restricted = restricted
        self.size_increment = size_increment
        self.type = type
        self.volume_usd24_h = volume_usd24_h

    @staticmethod
    def from_dict(obj: Any) -> 'Info':
        assert isinstance(obj, dict)
        ask = from_str(obj.get("ask"))
        base_currency = from_str(obj.get("baseCurrency"))
        bid = from_str(obj.get("bid"))
        change1_h = from_str(obj.get("change1h"))
        change24_h = from_str(obj.get("change24h"))
        change_bod = from_str(obj.get("changeBod"))
        enabled = from_str(obj.get("enabled"))
        high_leverage_fee_exempt = from_str(obj.get("highLeverageFeeExempt"))
        last = from_str(obj.get("last"))
        min_provide_size = from_str(obj.get("minProvideSize"))
        name = from_str(obj.get("name"))
        post_only = from_str(obj.get("postOnly"))
        price = from_str(obj.get("price"))
        price_increment = from_str(obj.get("priceIncrement"))
        quote_currency = from_str(obj.get("quoteCurrency"))
        quote_volume24_h = from_str(obj.get("quoteVolume24h"))
        restricted = from_str(obj.get("restricted"))
        size_increment = from_str(obj.get("sizeIncrement"))
        type = from_str(obj.get("type"))
        volume_usd24_h = from_str(obj.get("volumeUsd24h"))
        return Info(ask, base_currency, bid, change1_h, change24_h, change_bod, enabled, high_leverage_fee_exempt, last, min_provide_size, name, post_only, price, price_increment, quote_currency, quote_volume24_h, restricted, size_increment, type, volume_usd24_h)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ask"] = from_str(self.ask)
        result["baseCurrency"] = from_str(self.base_currency)
        result["bid"] = from_str(self.bid)
        result["change1h"] = from_str(self.change1_h)
        result["change24h"] = from_str(self.change24_h)
        result["changeBod"] = from_str(self.change_bod)
        result["enabled"] = from_str(self.enabled)
        result["highLeverageFeeExempt"] = from_str(self.high_leverage_fee_exempt)
        result["last"] = from_str(self.last)
        result["minProvideSize"] = from_str(self.min_provide_size)
        result["name"] = from_str(self.name)
        result["postOnly"] = from_str(self.post_only)
        result["price"] = from_str(self.price)
        result["priceIncrement"] = from_str(self.price_increment)
        result["quoteCurrency"] = from_str(self.quote_currency)
        result["quoteVolume24h"] = from_str(self.quote_volume24_h)
        result["restricted"] = from_str(self.restricted)
        result["sizeIncrement"] = from_str(self.size_increment)
        result["type"] = from_str(self.type)
        result["volumeUsd24h"] = from_str(self.volume_usd24_h)
        return result


class BchBtc:
    ask: float
    bid: float
    change: float
    close: float
    bch_btc_datetime: datetime
    info: Info
    last: float
    open: float
    percentage: float
    quote_volume: float
    symbol: str
    timestamp: int

    def __init__(self, ask: float, bid: float, change: float, close: float, bch_btc_datetime: datetime, info: Info, last: float, open: float, percentage: float, quote_volume: float, symbol: str, timestamp: int) -> None:
        self.ask = ask
        self.bid = bid
        self.change = change
        self.close = close
        self.bch_btc_datetime = bch_btc_datetime
        self.info = info
        self.last = last
        self.open = open
        self.percentage = percentage
        self.quote_volume = quote_volume
        self.symbol = symbol
        self.timestamp = timestamp

    @staticmethod
    def from_dict(obj: Any) -> 'BchBtc':
        assert isinstance(obj, dict)
        ask = from_float(obj.get("ask"))
        bid = from_float(obj.get("bid"))
        change = from_float(obj.get("change"))
        close = from_float(obj.get("close"))
        bch_btc_datetime = from_datetime(obj.get("datetime"))
        info = Info.from_dict(obj.get("info"))
        last = from_float(obj.get("last"))
        open = from_float(obj.get("open"))
        percentage = from_float(obj.get("percentage"))
        quote_volume = from_float(obj.get("quoteVolume"))
        symbol = from_str(obj.get("symbol"))
        timestamp = from_int(obj.get("timestamp"))
        return BchBtc(ask, bid, change, close, bch_btc_datetime, info, last, open, percentage, quote_volume, symbol, timestamp)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ask"] = to_float(self.ask)
        result["bid"] = to_float(self.bid)
        result["change"] = to_float(self.change)
        result["close"] = to_float(self.close)
        result["datetime"] = self.bch_btc_datetime.isoformat()
        result["info"] = to_class(Info, self.info)
        result["last"] = to_float(self.last)
        result["open"] = to_float(self.open)
        result["percentage"] = to_float(self.percentage)
        result["quoteVolume"] = to_float(self.quote_volume)
        result["symbol"] = from_str(self.symbol)
        result["timestamp"] = from_int(self.timestamp)
        return result


class CexTicker:
    bch_btc: BchBtc

    def __init__(self, bch_btc: BchBtc) -> None:
        self.bch_btc = bch_btc

    @staticmethod
    def from_dict(obj: Any) -> 'CexTicker':
        assert isinstance(obj, dict)
        bch_btc = BchBtc.from_dict(obj.get("BCH/BTC"))
        return CexTicker(bch_btc)

    def to_dict(self) -> dict:
        result: dict = {}
        result["BCH/BTC"] = to_class(BchBtc, self.bch_btc)
        return result


def cex_ticker_from_dict(s: Any) -> CexTicker:
    return CexTicker.from_dict(s)


def cex_ticker_to_dict(x: CexTicker) -> Any:
    return to_class(CexTicker, x)
