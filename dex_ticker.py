# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = dex_ticker_from_dict(json.loads(json_string))

from typing import Any, TypeVar, Type, cast


T = TypeVar("T")


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class APR:
    reward: float
    total: float

    def __init__(self, reward: float, total: float) -> None:
        self.reward = reward
        self.total = total

    @staticmethod
    def from_dict(obj: Any) -> 'APR':
        assert isinstance(obj, dict)
        reward = from_float(obj.get("reward"))
        total = from_float(obj.get("total"))
        return APR(reward, total)

    def to_dict(self) -> dict:
        result: dict = {}
        result["reward"] = to_float(self.reward)
        result["total"] = to_float(self.total)
        return result


class Creation:
    tx: str
    height: int

    def __init__(self, tx: str, height: int) -> None:
        self.tx = tx
        self.height = height

    @staticmethod
    def from_dict(obj: Any) -> 'Creation':
        assert isinstance(obj, dict)
        tx = from_str(obj.get("tx"))
        height = from_int(obj.get("height"))
        return Creation(tx, height)

    def to_dict(self) -> dict:
        result: dict = {}
        result["tx"] = from_str(self.tx)
        result["height"] = from_int(self.height)
        return result


class PriceRatio:
    ab: str
    ba: str

    def __init__(self, ab: str, ba: str) -> None:
        self.ab = ab
        self.ba = ba

    @staticmethod
    def from_dict(obj: Any) -> 'PriceRatio':
        assert isinstance(obj, dict)
        ab = from_str(obj.get("ab"))
        ba = from_str(obj.get("ba"))
        return PriceRatio(ab, ba)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ab"] = from_str(self.ab)
        result["ba"] = from_str(self.ba)
        return result


class Token:
    symbol: str
    display_symbol: str
    id: int
    reserve: str
    block_commission: int

    def __init__(self, symbol: str, display_symbol: str, id: int, reserve: str, block_commission: int) -> None:
        self.symbol = symbol
        self.display_symbol = display_symbol
        self.id = id
        self.reserve = reserve
        self.block_commission = block_commission

    @staticmethod
    def from_dict(obj: Any) -> 'Token':
        assert isinstance(obj, dict)
        symbol = from_str(obj.get("symbol"))
        display_symbol = from_str(obj.get("displaySymbol"))
        id = int(from_str(obj.get("id")))
        reserve = from_str(obj.get("reserve"))
        block_commission = float(from_str(obj.get("blockCommission")))
        return Token(symbol, display_symbol, id, reserve, block_commission)

    def to_dict(self) -> dict:
        result: dict = {}
        result["symbol"] = from_str(self.symbol)
        result["displaySymbol"] = from_str(self.display_symbol)
        result["id"] = from_str(str(self.id))
        result["reserve"] = from_str(self.reserve)
        result["blockCommission"] = from_str(str(self.block_commission))
        return result


class TotalLiquidity:
    token: str
    usd: str

    def __init__(self, token: str, usd: str) -> None:
        self.token = token
        self.usd = usd

    @staticmethod
    def from_dict(obj: Any) -> 'TotalLiquidity':
        assert isinstance(obj, dict)
        token = from_str(obj.get("token"))
        usd = from_str(obj.get("usd"))
        return TotalLiquidity(token, usd)

    def to_dict(self) -> dict:
        result: dict = {}
        result["token"] = from_str(self.token)
        result["usd"] = from_str(self.usd)
        return result


class Data:
    id: int
    symbol: str
    display_symbol: str
    name: str
    status: bool
    token_a: Token
    token_b: Token
    price_ratio: PriceRatio
    commission: str
    total_liquidity: TotalLiquidity
    trade_enabled: bool
    owner_address: str
    reward_pct: str
    creation: Creation
    apr: APR

    def __init__(self, id: int, symbol: str, display_symbol: str, name: str, status: bool, token_a: Token, token_b: Token, price_ratio: PriceRatio, commission: str, total_liquidity: TotalLiquidity, trade_enabled: bool, owner_address: str, reward_pct: str, creation: Creation, apr: APR) -> None:
        self.id = id
        self.symbol = symbol
        self.display_symbol = display_symbol
        self.name = name
        self.status = status
        self.token_a = token_a
        self.token_b = token_b
        self.price_ratio = price_ratio
        self.commission = commission
        self.total_liquidity = total_liquidity
        self.trade_enabled = trade_enabled
        self.owner_address = owner_address
        self.reward_pct = reward_pct
        self.creation = creation
        self.apr = apr

    @staticmethod
    def from_dict(obj: Any) -> 'Data':
        assert isinstance(obj, dict)
        id = int(from_str(obj.get("id")))
        symbol = from_str(obj.get("symbol"))
        display_symbol = from_str(obj.get("displaySymbol"))
        name = from_str(obj.get("name"))
        status = from_bool(obj.get("status"))
        token_a = Token.from_dict(obj.get("tokenA"))
        token_b = Token.from_dict(obj.get("tokenB"))
        price_ratio = PriceRatio.from_dict(obj.get("priceRatio"))
        commission = from_str(obj.get("commission"))
        total_liquidity = TotalLiquidity.from_dict(obj.get("totalLiquidity"))
        trade_enabled = from_bool(obj.get("tradeEnabled"))
        owner_address = from_str(obj.get("ownerAddress"))
        reward_pct = from_str(obj.get("rewardPct"))
        creation = Creation.from_dict(obj.get("creation"))
        apr = APR.from_dict(obj.get("apr"))
        return Data(id, symbol, display_symbol, name, status, token_a, token_b, price_ratio, commission, total_liquidity, trade_enabled, owner_address, reward_pct, creation, apr)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(str(self.id))
        result["symbol"] = from_str(self.symbol)
        result["displaySymbol"] = from_str(self.display_symbol)
        result["name"] = from_str(self.name)
        result["status"] = from_bool(self.status)
        result["tokenA"] = to_class(Token, self.token_a)
        result["tokenB"] = to_class(Token, self.token_b)
        result["priceRatio"] = to_class(PriceRatio, self.price_ratio)
        result["commission"] = from_str(self.commission)
        result["totalLiquidity"] = to_class(TotalLiquidity, self.total_liquidity)
        result["tradeEnabled"] = from_bool(self.trade_enabled)
        result["ownerAddress"] = from_str(self.owner_address)
        result["rewardPct"] = from_str(self.reward_pct)
        result["creation"] = to_class(Creation, self.creation)
        result["apr"] = to_class(APR, self.apr)
        return result


class DexTicker:
    data: Data

    def __init__(self, data: Data) -> None:
        self.data = data

    @staticmethod
    def from_dict(obj: Any) -> 'DexTicker':
        assert isinstance(obj, dict)
        data = Data.from_dict(obj.get("data"))
        return DexTicker(data)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = to_class(Data, self.data)
        return result


def dex_ticker_from_dict(s: Any) -> DexTicker:
    return DexTicker.from_dict(s)


def dex_ticker_to_dict(x: DexTicker) -> Any:
    return to_class(DexTicker, x)
