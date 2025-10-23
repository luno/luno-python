import os
import time

from luno_python.client import Client

if __name__ == "__main__":
    c = Client(api_key_id=os.getenv("LUNO_API_KEY_ID"), api_key_secret=os.getenv("LUNO_API_KEY_SECRET"))

    res = c.get_tickers()
    print(res)
    time.sleep(0.5)

    res = c.get_ticker(pair="XBTZAR")
    print(res)
    time.sleep(0.5)

    res = c.get_order_book(pair="XBTZAR")
    print(res)
    time.sleep(0.5)

    since = int(time.time() * 1000) - 24 * 60 * 59 * 1000
    res = c.list_trades(pair="XBTZAR", since=since)
    print(res)
    time.sleep(0.5)

    res = c.get_candles(pair="XBTZAR", since=since, duration=300)
    print(res)
    time.sleep(0.5)

    res = c.get_balances()
    print(res)
    time.sleep(0.5)

    aid = ""
    if res["balance"]:
        aid = res["balance"][0]["account_id"]

    if aid:
        res = c.list_transactions(id=aid, min_row=1, max_row=10)
        print(res)
        time.sleep(0.5)

    if aid:
        res = c.list_pending_transactions(id=aid)
        print(res)
        time.sleep(0.5)

    res = c.list_orders()
    print(res)
    time.sleep(0.5)

    res = c.list_user_trades(pair="XBTZAR")
    print(res)
    time.sleep(0.5)

    res = c.get_fee_info(pair="XBTZAR")
    print(res)
    time.sleep(0.5)

    res = c.get_funding_address(asset="XBT")
    print(res)
    time.sleep(0.5)

    res = c.list_withdrawals()
    print(res)
    time.sleep(0.5)

    wid = ""
    if res["withdrawals"]:
        wid = res["withdrawals"][0]["id"]

    if wid:
        res = c.get_withdrawal(id=wid)
        print(res)
        time.sleep(0.5)
