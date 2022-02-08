# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = welcome_from_dict(json.loads(json_string))

from typing import Optional, Any, TypeVar, Type, cast


T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Oracles:
    active: Optional[int]
    total: Optional[int]

    def __init__(self, active: Optional[int], total: Optional[int]) -> None:
        self.active = active
        self.total = total

    @staticmethod
    def from_dict(obj: Any) -> 'Oracles':
        assert isinstance(obj, dict)
        active = from_union([from_int, from_none], obj.get("active"))
        total = from_union([from_int, from_none], obj.get("total"))
        return Oracles(active, total)

    def to_dict(self) -> dict:
        result: dict = {}
        result["active"] = from_union([from_int, from_none], self.active)
        result["total"] = from_union([from_int, from_none], self.total)
        return result


class Aggregated:
    amount: Optional[str]
    weightage: Optional[int]
    oracles: Optional[Oracles]

    def __init__(self, amount: Optional[str], weightage: Optional[int], oracles: Optional[Oracles]) -> None:
        self.amount = amount
        self.weightage = weightage
        self.oracles = oracles

    @staticmethod
    def from_dict(obj: Any) -> 'Aggregated':
        assert isinstance(obj, dict)
        amount = from_union([from_str, from_none], obj.get("amount"))
        weightage = from_union([from_int, from_none], obj.get("weightage"))
        oracles = from_union([Oracles.from_dict, from_none], obj.get("oracles"))
        return Aggregated(amount, weightage, oracles)

    def to_dict(self) -> dict:
        result: dict = {}
        result["amount"] = from_union([from_str, from_none], self.amount)
        result["weightage"] = from_union([from_int, from_none], self.weightage)
        result["oracles"] = from_union([lambda x: to_class(Oracles, x), from_none], self.oracles)
        return result


class Block:
    hash: Optional[str]
    height: Optional[int]
    median_time: Optional[int]
    time: Optional[int]

    def __init__(self, hash: Optional[str], height: Optional[int], median_time: Optional[int], time: Optional[int]) -> None:
        self.hash = hash
        self.height = height
        self.median_time = median_time
        self.time = time

    @staticmethod
    def from_dict(obj: Any) -> 'Block':
        assert isinstance(obj, dict)
        hash = from_union([from_str, from_none], obj.get("hash"))
        height = from_union([from_int, from_none], obj.get("height"))
        median_time = from_union([from_int, from_none], obj.get("medianTime"))
        time = from_union([from_int, from_none], obj.get("time"))
        return Block(hash, height, median_time, time)

    def to_dict(self) -> dict:
        result: dict = {}
        result["hash"] = from_union([from_str, from_none], self.hash)
        result["height"] = from_union([from_int, from_none], self.height)
        result["medianTime"] = from_union([from_int, from_none], self.median_time)
        result["time"] = from_union([from_int, from_none], self.time)
        return result


class Price:
    block: Optional[Block]
    aggregated: Optional[Aggregated]
    currency: Optional[str]
    token: Optional[str]
    id: Optional[str]
    key: Optional[str]
    sort: Optional[str]

    def __init__(self, block: Optional[Block], aggregated: Optional[Aggregated], currency: Optional[str], token: Optional[str], id: Optional[str], key: Optional[str], sort: Optional[str]) -> None:
        self.block = block
        self.aggregated = aggregated
        self.currency = currency
        self.token = token
        self.id = id
        self.key = key
        self.sort = sort

    @staticmethod
    def from_dict(obj: Any) -> 'Price':
        assert isinstance(obj, dict)
        block = from_union([Block.from_dict, from_none], obj.get("block"))
        aggregated = from_union([Aggregated.from_dict, from_none], obj.get("aggregated"))
        currency = from_union([from_str, from_none], obj.get("currency"))
        token = from_union([from_str, from_none], obj.get("token"))
        id = from_union([from_str, from_none], obj.get("id"))
        key = from_union([from_str, from_none], obj.get("key"))
        sort = from_union([from_str, from_none], obj.get("sort"))
        return Price(block, aggregated, currency, token, id, key, sort)

    def to_dict(self) -> dict:
        result: dict = {}
        result["block"] = from_union([lambda x: to_class(Block, x), from_none], self.block)
        result["aggregated"] = from_union([lambda x: to_class(Aggregated, x), from_none], self.aggregated)
        result["currency"] = from_union([from_str, from_none], self.currency)
        result["token"] = from_union([from_str, from_none], self.token)
        result["id"] = from_union([from_str, from_none], self.id)
        result["key"] = from_union([from_str, from_none], self.key)
        result["sort"] = from_union([from_str, from_none], self.sort)
        return result


class Data:
    id: Optional[str]
    sort: Optional[str]
    price: Optional[Price]

    def __init__(self, id: Optional[str], sort: Optional[str], price: Optional[Price]) -> None:
        self.id = id
        self.sort = sort
        self.price = price

    @staticmethod
    def from_dict(obj: Any) -> 'Data':
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("id"))
        sort = from_union([from_str, from_none], obj.get("sort"))
        price = from_union([Price.from_dict, from_none], obj.get("price"))
        return Data(id, sort, price)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_str, from_none], self.id)
        result["sort"] = from_union([from_str, from_none], self.sort)
        result["price"] = from_union([lambda x: to_class(Price, x), from_none], self.price)
        return result


class DfiOracleTicker:
    data: Optional[Data]

    def __init__(self, data: Optional[Data]) -> None:
        self.data = data

    @staticmethod
    def from_dict(obj: Any) -> 'DfiOracleTicker':
        assert isinstance(obj, dict)
        data = from_union([Data.from_dict, from_none], obj.get("data"))
        return DfiOracleTicker(data)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = from_union([lambda x: to_class(Data, x), from_none], self.data)
        return result


def dfi_oracle_ticker_from_dict(s: Any) -> DfiOracleTicker:
    return DfiOracleTicker.from_dict(s)


def dfi_oracle_ticker_to_dict(x: DfiOracleTicker) -> Any:
    return to_class(DfiOracleTicker, x)
