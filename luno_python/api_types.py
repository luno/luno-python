from collections import namedtuple
from decimal import Decimal
from typing import List

DEC_0 = Decimal("0")

Order = namedtuple("Order", "order_id price volume")

MarketState = namedtuple("MarketState", "sequence asks bids status")

Pair = namedtuple("Pair", "base counter")

def format_orderbook(pair: Pair, asks: List[Order], bids: List[Order]):
    if not bids or not asks:
        return "Empty Orderbook"

    bid_sum = sum((o.price * o.volume for o in bids), DEC_0)
    ask_sum = sum((o.volume for o in asks), DEC_0)

    mid = (asks[0].price + bids[0].price) / 2

    return f"{bid_sum} {pair.counter} - {mid} - {ask_sum} {pair.base}"

def format_state(pair: Pair, state: MarketState):
    orderbook = format_orderbook(pair, state.asks, state.bids)
    return f"[{state.sequence}] {orderbook}"
