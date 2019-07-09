"""
The stream client can be used to receive live updates to the orderbook.
It also maintains a representation of the Luno orderbook correctly updated for each event.

For example usage see examples/stream.py
"""

import asyncio
from decimal import Decimal
import json
from typing import Callable, Dict, List
import websockets

from .api_types import DEC_0, Order, MarketState, Pair

DEFAULT_URL = "wss://ws.luno.com"

StateUpdate = Callable[[Pair, MarketState, dict], None]

class OutOfOrderMessageException(Exception):
    pass


def _flatten_orders(orders, reverse):
    return sorted(orders.values(), key=lambda o: o.price, reverse=reverse)


def _decrement_trade(orders: Dict[str, Order], order_id: str, volume: Decimal):
    order = orders.pop(order_id, None)
    if order is None:
        return

    new_order = order._replace(volume=order.volume - volume)
    if new_order.volume > DEC_0:
        orders[order_id] = new_order


class _MarketStreamState:
    def __init__(self, first: dict):
        if first is None:
            raise Exception("Unable to use empty message to initialise market state")

        def conv_message(msg):
            return Order(
                msg['id'],
                Decimal(msg['price']),
                Decimal(msg['volume']),
            )

        bids = [conv_message(m) for m in first['bids']]
        asks = [conv_message(m) for m in first['asks']]
        self._bids = {b.order_id: b for b in bids}
        self._asks = {a.order_id: a for a in asks}
        self._sequence = first['sequence']
        self._trades = []
        self._status = first['status']

    def get_asks(self):
        return _flatten_orders(self._asks, False)

    def get_bids(self):
        return _flatten_orders(self._bids, True)

    def get_status(self):
        return self._status

    def get_sequence(self):
        return self._sequence

    def get_snapshot(self):
        return MarketState(
            sequence=self.get_sequence(),
            asks=self.get_asks(),
            bids=self.get_bids(),
            status=self.get_status(),
        )

    def process_update(self, update: dict):
        if update is None:
            return

        seq = update['sequence']
        if seq <= self._sequence:
            raise OutOfOrderMessageException()

        trades = update.get('trade_updates')
        if trades:
            self._process_trades(trades)

        create = update.get('create_update')
        if create:
            self._process_create(create)

        delete_upd = update.get('delete_update')
        if delete_upd:
            self._process_delete(delete_upd)

        status_upd = update.get('status_update')
        if status_upd:
            self._process_status(status_upd)

        self._sequence = seq

    def _process_trades(self, trade_updates: List[dict]):
        for t in trade_updates:
            maker_id = t['maker_order_id']
            volume = Decimal(t['base'])

            _decrement_trade(self._asks, maker_id, volume)
            _decrement_trade(self._bids, maker_id, volume)

    def _process_create(self, create_update: dict):
        o = Order(
            create_update['order_id'],
            Decimal(create_update['price']),
            Decimal(create_update['volume']),
        )
        if create_update['type'] == "ASK":
            self._asks[o.order_id] = o
        elif create_update['type'] == "BID":
            self._bids[o.order_id] = o

    def _process_delete(self, delete_update: dict):
        order_id = delete_update['order_id']
        self._asks.pop(order_id, None)
        self._bids.pop(order_id, None)

    def _process_status(self, status_update: dict):
        self._status = status_update['status']


async def _read_from_websocket(ws, pair: Pair, update_f: StateUpdate):
    state = None
    is_first = True

    async for message in ws:
        try:
            body = json.loads(message)
        except ValueError:
            raise Exception(message)

        if body == "": # Empty update, used as keepalive
            body = None

        if is_first:
            is_first = False
            state = _MarketStreamState(body)
            update_f(pair, state.get_snapshot(), None)
            continue

        try:
            state.process_update(body)
        except OutOfOrderMessageException:
            continue

        update_f(pair, state.get_snapshot(), body)


async def _write_keep_alive(ws):
    while True:
        await ws.send('""')
        await asyncio.sleep(60)


async def stream_market(
        pair: str,
        api_key_id: str,
        api_key_secret: str,
        update_callback: StateUpdate,
        base_url: str = DEFAULT_URL,
):
    """Opens a stream to /api/1/stream/...

        Stream orderbook information and maintain an orderbook state.

        :param pair: str Amount to buy or sell in the pair base currency.
        :param api_key_id: str
        :param api_key_secret: str
        :param update_callback: an StateUpdate function that will be called with new updates.
    """
    if len(pair) != 6:
        raise Exception("Invalid pair")

    p = Pair(pair[:3].upper(), pair[3:].upper())
    url = '/'.join([base_url, 'api/1/stream', p.base + p.counter])

    async with websockets.connect(
            url,
            origin='http://localhost/',
            ping_interval=None,
    ) as websocket:

        auth = json.dumps({
            'api_key_id': api_key_id,
            'api_key_secret': api_key_secret,
        })
        await websocket.send(auth)

        await asyncio.gather(
            _read_from_websocket(websocket, p, update_callback),
            _write_keep_alive(websocket),
        )
