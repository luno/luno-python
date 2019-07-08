import asyncio

from luno_python.stream_client import stream_market
from luno_python.api_types import format_state

def handle_update(pair, state, update):
    print(format_state(pair, state))
    if update is not None:
        print(update)

asyncio.get_event_loop().run_until_complete(
    stream_market(
        pair="XBTZAR",
        api_key_id=[api key],
        api_key_secret=[api secret],
        update_callback=handle_update,
    )
)
