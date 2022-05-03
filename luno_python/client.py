from .base_client import BaseClient


class Client(BaseClient):
    """
    Python SDK for the Luno API.

    Example usage:

      from luno_python.client import Client


      c = Client(api_key_id='key_id', api_key_secret='key_secret')
      try:
        res = c.get_ticker(pair='XBTZAR')
        print res
      except Exception as e:
        print e
    """

    def cancel_withdrawal(self, id):
        """Makes a call to DELETE /api/1/withdrawals/{id}.

        Cancels a withdrawal request.
        This can only be done if the request is still in state <code>PENDING</code>.

        Permissions required: <code>Perm_W_Withdrawals</code>

        :param id: ID of the withdrawal to cancel.
        :type id: int
        """
        req = {
            'id': id,
        }
        return self.do('DELETE', '/api/1/withdrawals/{id}', req=req, auth=True)

    def create_account(self, currency, name):
        """Makes a call to POST /api/1/accounts.

        This request creates an Account for the specified currency.  Please note that the balances for the Account will be displayed based on the <code>asset</code> value, which is the currency the Account is based on.

        Permissions required: <code>Perm_W_Addresses</code>

        :param currency: The currency code for the Account you want to create.  Please see the Currency section for a detailed list of currencies supported by the Luno platform.

                         Users must be verified to trade currency in order to be able to create an Account.  For more information on the verification process, please see <a href="/help/en/articles/1000168396">How do I verify my identity?</a>.

                         Users have a limit of 4 accounts per currency.
        :type currency: str
        :param name: The label to use for this account
        :type name: str
        """
        req = {
            'currency': currency,
            'name': name,
        }
        return self.do('POST', '/api/1/accounts', req=req, auth=True)

    def create_funding_address(self, asset, name=None):
        """Makes a call to POST /api/1/funding_address.

        Allocates a new receive address to your account. There is a rate limit of 1
        address per hour, but bursts of up to 10 addresses are allowed. Only 1
        Ethereum receive address can be created.

        Permissions required: <code>Perm_W_Addresses</code>

        :param asset: Currency code of the asset.
        :type asset: str
        :param name: An optional name for the new Receive Address
        :type name: str
        """
        req = {
            'asset': asset,
            'name': name,
        }
        return self.do('POST', '/api/1/funding_address', req=req, auth=True)

    def create_withdrawal(self, amount, type, beneficiary_id=None, external_id=None, fast=None, reference=None):
        """Makes a call to POST /api/1/withdrawals.

        Creates a new withdrawal request to the specified beneficiary.

        Permissions required: <code>Perm_W_Withdrawals</code>

        :param amount: Amount to withdraw. The currency withdrawn depends on the type setting.
        :type amount: float
        :param type: Withdrawal method.
        :type type: str
        :param beneficiary_id: The beneficiary ID of the bank account the withdrawal will be paid out to.
                               This parameter is required if the user has set up multiple beneficiaries.
                               The beneficiary ID can be found by selecting on the beneficiary name on the user’s <a href="/wallet/beneficiaries">Beneficiaries</a> page.
        :type beneficiary_id: int
        :param external_id: Optional unique ID to associate with this withdrawal.
                            Useful to prevent duplicate sends.
                            This field supports all alphanumeric characters including "-" and "_".
        :type external_id: str
        :param fast: If true, it will be a fast withdrawal if possible. Fast withdrawals come with a fee.
                     Currently fast withdrawals are only available for `type=ZAR_EFT`; for other types, an error is returned.
                     Fast withdrawals are not possible for Bank of Baroda, Deutsche Bank, Merrill Lynch South Africa, UBS, Postbank and Tyme Bank.
                     The fee to be charged is the same as when withdrawing from the UI.
        :type fast: bool
        :param reference: For internal use.
        :type reference: str
        """
        req = {
            'amount': amount,
            'type': type,
            'beneficiary_id': beneficiary_id,
            'external_id': external_id,
            'fast': fast,
            'reference': reference,
        }
        return self.do('POST', '/api/1/withdrawals', req=req, auth=True)

    def get_balances(self, assets=None):
        """Makes a call to GET /api/1/balance.

        The list of all Accounts and their respective balances for the requesting user.

        Permissions required: <code>Perm_R_Balance</code>

        :param assets: Only return balances for wallets with these currencies (if not provided,
                       all balances will be returned). To request balances for multiple currencies,
                       pass the parameter multiple times,
                       e.g. `assets=XBT&assets=ETH`.
        :type assets: list
        """
        req = {
            'assets': assets,
        }
        return self.do('GET', '/api/1/balance', req=req, auth=True)

    def get_candles(self, duration, pair, since):
        """Makes a call to GET /api/exchange/1/candles.

        Get candlestick market data from the specified time until now, from the oldest to the most recent.

        Permissions required: <code>MP_None</code>

        :param duration: Candle duration in seconds.
                         For example, 300 corresponds to 5m candles. Currently supported
                         durations are: 60 (1m), 300 (5m), 900 (15m), 1800 (30m), 3600 (1h),
                         10800 (3h), 14400 (4h), 28800 (8h), 86400 (24h), 259200 (3d), 604800
                         (7d).
        :type duration: int
        :param pair: Currency pair
        :type pair: str
        :param since: Filter to candles starting on or after this timestamp (Unix milliseconds).
                      Only up to 1000 of the earliest candles are returned.
        :type since: int
        """
        req = {
            'duration': duration,
            'pair': pair,
            'since': since,
        }
        return self.do('GET', '/api/exchange/1/candles', req=req, auth=True)

    def get_fee_info(self, pair):
        """Makes a call to GET /api/1/fee_info.

        Returns the fees and 30 day trading volume (as of midnight) for a given currency pair.  For complete details, please see <a href="en/countries">Fees & Features</a>.

        Permissions required: <code>Perm_R_Orders</code>

        :param pair: Get fee information about this pair.
        :type pair: str
        """
        req = {
            'pair': pair,
        }
        return self.do('GET', '/api/1/fee_info', req=req, auth=True)

    def get_funding_address(self, asset, address=None):
        """Makes a call to GET /api/1/funding_address.

        Returns the default receive address associated with your account and the
        amount received via the address. Users can specify an optional address parameter to return information for a non-default receive address.

        In the response, <code>total_received</code> is the total confirmed amount received excluding unconfirmed transactions.
        <code>total_unconfirmed</code> is the total sum of unconfirmed receive transactions.

        Permissions required: <code>Perm_R_Addresses</code>

        :param asset: Currency code of the asset.
        :type asset: str
        :param address: Specific cryptocurrency address to retrieve. If not provided, the
                        default address will be used.
        :type address: str
        """
        req = {
            'asset': asset,
            'address': address,
        }
        return self.do('GET', '/api/1/funding_address', req=req, auth=True)

    def get_move(self, client_move_id=None, id=None):
        """Makes a call to GET /api/exchange/1/move.

        Get a specific move funds instruction by either <code>id</code> or
        <code>client_move_id</code>. If both are provided an API error will be
        returned.

        This endpoint is in BETA, behaviour and specification may change without
        any previous notice.

        Permissions required: <code>MP_None</code>

        :param client_move_id: Get by the user defined ID. This is mutually exclusive with <code>id</code> and is required if <code>id</code> is
                               not provided.
        :type client_move_id: str
        :param id: Get by the system ID. This is mutually exclusive with <code>client_move_id</code> and is required if
                   <code>client_move_id</code> is not provided.
        :type id: str
        """
        req = {
            'client_move_id': client_move_id,
            'id': id,
        }
        return self.do('GET', '/api/exchange/1/move', req=req, auth=True)

    def get_order(self, id):
        """Makes a call to GET /api/1/orders/{id}.

        Get an Order's details by its ID.

        Permissions required: <code>Perm_R_Orders</code>

        :param id: Order reference
        :type id: str
        """
        req = {
            'id': id,
        }
        return self.do('GET', '/api/1/orders/{id}', req=req, auth=True)

    def get_order_book(self, pair):
        """Makes a call to GET /api/1/orderbook_top.

        This request returns the best 100 `bids` and `asks`, for the currency pair specified, in the Order Book.

        `asks` are sorted by price ascending and `bids` are sorted by price descending.

        Multiple orders at the same price are aggregated.

        :param pair: Currency pair of the Orders to retrieve
        :type pair: str
        """
        req = {
            'pair': pair,
        }
        return self.do('GET', '/api/1/orderbook_top', req=req, auth=False)

    def get_order_book_full(self, pair):
        """Makes a call to GET /api/1/orderbook.

        This request returns all `bids` and `asks`, for the currency pair specified, in the Order Book.

        `asks` are sorted by price ascending and `bids` are sorted by price descending.

        Multiple orders at the same price are not aggregated.

        <b>WARNING:</b> This may return a large amount of data.
        Users are recommended to use the <a href="#operation/getOrderBookTop">top 100 bids and asks</a>
        or the <a href="#tag/Streaming-API">Streaming API</a>.

        :param pair: Currency pair of the Orders to retrieve
        :type pair: str
        """
        req = {
            'pair': pair,
        }
        return self.do('GET', '/api/1/orderbook', req=req, auth=False)

    def get_order_v2(self, id):
        """Makes a call to GET /api/exchange/2/orders/{id}.

        Get the details for an order.

        Permissions required: <code>Perm_R_Orders</code>

        :param id: Order reference
        :type id: str
        """
        req = {
            'id': id,
        }
        return self.do('GET', '/api/exchange/2/orders/{id}', req=req, auth=True)

    def get_order_v3(self, client_order_id=None, id=None):
        """Makes a call to GET /api/exchange/3/order.

        Get the details for an order by order reference or client order ID.
        Exactly one of the two parameters must be provided, otherwise an error is returned.
        Permissions required: <code>Perm_R_Orders</code>

        :param client_order_id: Client Order ID has the value that was passed in when the Order was posted.
        :type client_order_id: str
        :param id: Order reference
        :type id: str
        """
        req = {
            'client_order_id': client_order_id,
            'id': id,
        }
        return self.do('GET', '/api/exchange/3/order', req=req, auth=True)

    def get_ticker(self, pair):
        """Makes a call to GET /api/1/ticker.

        Returns the latest ticker indicators for the specified currency pair.

        Please see the <a href="#tag/currency ">Currency list</a> for the complete list of supported currency pairs.

        :param pair: Currency pair
        :type pair: str
        """
        req = {
            'pair': pair,
        }
        return self.do('GET', '/api/1/ticker', req=req, auth=False)

    def get_tickers(self, pair=None):
        """Makes a call to GET /api/1/tickers.

        Returns the latest ticker indicators from all active Luno exchanges.

        Please see the <a href="#tag/currency ">Currency list</a> for the complete list of supported currency pairs.

        :param pair: Return tickers for multiple markets (if not provided, all tickers will be returned).
                     To request tickers for multiple markets, pass the parameter multiple times,
                     e.g. `pair=XBTZAR&pair=ETHZAR`.
        :type pair: list
        """
        req = {
            'pair': pair,
        }
        return self.do('GET', '/api/1/tickers', req=req, auth=False)

    def get_withdrawal(self, id):
        """Makes a call to GET /api/1/withdrawals/{id}.

        Returns the status of a particular withdrawal request.

        Permissions required: <code>Perm_R_Withdrawals</code>

        :param id: Withdrawal ID to retrieve.
        :type id: int
        """
        req = {
            'id': id,
        }
        return self.do('GET', '/api/1/withdrawals/{id}', req=req, auth=True)

    def list_beneficiaries_response(self):
        """Makes a call to GET /api/1/beneficiaries.

        Returns a list of bank beneficiaries.

        Permissions required: <code>Perm_R_Beneficiaries</code>

        """
        return self.do('GET', '/api/1/beneficiaries', req=None, auth=True)

    def list_moves(self, before=None, limit=None):
        """Makes a call to GET /api/exchange/1/move/list_moves.

        Returns a list of the most recent moves ordered from newest to oldest.
        This endpoint will list up to 100 most recent moves by default.

        This endpoint is in BETA, behaviour and specification may change without
        any previous notice.

        Permissions required: <code>MP_None</code>

        :param before: Filter to moves requested before this timestamp (Unix milliseconds)
        :type before: int
        :param limit: Limit to this many moves
        :type limit: int
        """
        req = {
            'before': before,
            'limit': limit,
        }
        return self.do('GET', '/api/exchange/1/move/list_moves', req=req, auth=True)

    def list_orders(self, created_before=None, limit=None, pair=None, state=None):
        """Makes a call to GET /api/1/listorders.

        Returns a list of the most recently placed Orders.
        Users can specify an optional <code>state=PENDING</code> parameter to restrict the results to only open Orders.
        Users can also specify the market by using the optional currency pair parameter.

        Permissions required: <code>Perm_R_Orders</code>

        :param created_before: Filter to orders created before this timestamp (Unix milliseconds)
        :type created_before: int
        :param limit: Limit to this many orders
        :type limit: int
        :param pair: Filter to only orders of this currency pair
        :type pair: str
        :param state: Filter to only orders of this state
        :type state: str
        """
        req = {
            'created_before': created_before,
            'limit': limit,
            'pair': pair,
            'state': state,
        }
        return self.do('GET', '/api/1/listorders', req=req, auth=True)

    def list_orders_v2(self, closed=None, created_before=None, limit=None, pair=None):
        """Makes a call to GET /api/exchange/2/listorders.

        Returns a list of the most recently placed orders ordered from newest to
        oldest. This endpoint will list up to 100 most recent open orders by
        default.

        Permissions required: <Code>Perm_R_Orders</Code>

        :param closed: If true, will return closed orders instead of open orders.
        :type closed: bool
        :param created_before: Filter to orders created before this timestamp (Unix milliseconds)
        :type created_before: int
        :param limit: Limit to this many orders
        :type limit: int
        :param pair: Filter to only orders of this currency pair.
        :type pair: str
        """
        req = {
            'closed': closed,
            'created_before': created_before,
            'limit': limit,
            'pair': pair,
        }
        return self.do('GET', '/api/exchange/2/listorders', req=req, auth=True)

    def list_pending_transactions(self, id):
        """Makes a call to GET /api/1/accounts/{id}/pending.

        Return a list of all transactions that have not completed for the Account.

        Pending transactions are not numbered, and may be reordered, deleted or updated at any time.

        Permissions required: <code>Perm_R_Transactions</code>

        :param id: Account ID
        :type id: int
        """
        req = {
            'id': id,
        }
        return self.do('GET', '/api/1/accounts/{id}/pending', req=req, auth=True)

    def list_trades(self, pair, since=None):
        """Makes a call to GET /api/1/trades.

        Returns a list of recent trades for the specified currency pair. At most
        100 trades are returned per call and never trades older than 24h. The
        trades are sorted from newest to oldest.

        Please see the <a href="#tag/currency ">Currency list</a> for the complete list of supported currency pairs.

        :param pair: Currency pair of the market to list the trades from
        :type pair: str
        :param since: Fetch trades executed after this time, specified as a Unix timestamp in
                      milliseconds. An error will be returned if this is before 24h ago. Use
                      this parameter to either restrict to a shorter window or to iterate over
                      the trades in case you need more than the 100 most recent trades.
        :type since: int
        """
        req = {
            'pair': pair,
            'since': since,
        }
        return self.do('GET', '/api/1/trades', req=req, auth=False)

    def list_transactions(self, id, max_row, min_row):
        """Makes a call to GET /api/1/accounts/{id}/transactions.

        Return a list of transaction entries from an account.

        Transaction entry rows are numbered sequentially starting from 1, where 1 is
        the oldest entry. The range of rows to return are specified with the
        <code>min_row</code> (inclusive) and <code>max_row</code> (exclusive)
        parameters. At most 1000 rows can be requested per call.

        If <code>min_row</code> or <code>max_row</code> is non-positive, the range
        wraps around the most recent row. For example, to fetch the 100 most recent
        rows, use <code>min_row=-100</code> and <code>max_row=0</code>.

        Permissions required: <code>Perm_R_Transactions</code>

        :param id: Account ID - the unique identifier for the specific Account.
        :type id: int
        :param max_row: Maximum of the row range to return (exclusive)
        :type max_row: int
        :param min_row: Minimum of the row range to return (inclusive)
        :type min_row: int
        """
        req = {
            'id': id,
            'max_row': max_row,
            'min_row': min_row,
        }
        return self.do('GET', '/api/1/accounts/{id}/transactions', req=req, auth=True)

    def list_transfers(self, account_id, before=None, limit=None):
        """Makes a call to GET /api/exchange/1/transfers.

        Returns a list of the most recent confirmed transfers ordered from newest to
        oldest.
        This includes bank transfers, card payments, or on-chain transactions that
        have been reflected on your account available balance.

        Note that the Transfer `amount` is always a positive value and you should
        use the `inbound` flag to determine the direction of the transfer.

        If you need to paginate the results you can set the `before` parameter to
        the last returned transfer `created_at` field value and repeat the request
        until you have all the transfers you need.
        This endpoint will list up to 100 transfers at a time by default.

        This endpoint is in BETA, behaviour and specification may change without
        any previous notice.

        Permissions required: <Code>Perm_R_Transfers</Code>

        :param account_id: Unique identifier of the account to list the transfers from.
        :type account_id: int
        :param before: Filter to transfers created before this timestamp (Unix milliseconds).
                       The default value (0) will return the latest transfers on the account.
        :type before: int
        :param limit: Limit to this many transfers.
        :type limit: int
        """
        req = {
            'account_id': account_id,
            'before': before,
            'limit': limit,
        }
        return self.do('GET', '/api/exchange/1/transfers', req=req, auth=True)

    def list_user_trades(self, pair, after_seq=None, before=None, before_seq=None, limit=None, since=None, sort_desc=None):
        """Makes a call to GET /api/1/listtrades.

        Returns a list of the recent Trades for a given currency pair for this user, sorted by oldest first.
        If <code>before</code> is specified, then Trades are returned sorted by most-recent first.

        <code>type</code> in the response indicates the type of Order that was placed to participate in the trade.
        Possible types: <code>BID</code>, <code>ASK</code>.

        If <code>is_buy</code> in the response is true, then the Order which completed the trade (market taker) was a Bid Order.

        Results of this query may lag behind the latest data.

        Permissions required: <code>Perm_R_Orders</code>

        :param pair: Filter to trades of this currency pair.
        :type pair: str
        :param after_seq: Filter to trades from (including) this sequence number.
                          Default behaviour is not to include this filter.
        :type after_seq: int
        :param before: Filter to trades before this timestamp (Unix milliseconds).
        :type before: int
        :param before_seq: Filter to trades before (excluding) this sequence number.
                           Default behaviour is not to include this filter.
        :type before_seq: int
        :param limit: Limit to this number of trades (default 100).
        :type limit: int
        :param since: Filter to trades on or after this timestamp (Unix milliseconds).
        :type since: int
        :param sort_desc: If set to true, sorts trades in descending order, otherwise ascending
                          order will be assumed.
        :type sort_desc: bool
        """
        req = {
            'pair': pair,
            'after_seq': after_seq,
            'before': before,
            'before_seq': before_seq,
            'limit': limit,
            'since': since,
            'sort_desc': sort_desc,
        }
        return self.do('GET', '/api/1/listtrades', req=req, auth=True)

    def list_withdrawals(self, before_id=None, limit=None):
        """Makes a call to GET /api/1/withdrawals.

        Returns a list of withdrawal requests.

        Permissions required: <code>Perm_R_Withdrawals</code>

        :param before_id: Filter to withdrawals requested on or before the withdrawal with this ID.
                          Can be used for pagination.
        :type before_id: int
        :param limit: Limit to this many withdrawals
        :type limit: int
        """
        req = {
            'before_id': before_id,
            'limit': limit,
        }
        return self.do('GET', '/api/1/withdrawals', req=req, auth=True)

    def markets(self):
        """Makes a call to GET /api/exchange/1/markets.

        List all supported markets parameter information like price scale, min and
        max order volumes and market ID.

        """
        return self.do('GET', '/api/exchange/1/markets', req=None, auth=False)

    def move(self, amount, credit_account_id, debit_account_id, client_move_id=None):
        """Makes a call to POST /api/exchange/1/move.

        Move funds between two of your accounts with the same currency
        The funds may not be moved by the time the request returns. The GET method
        can be used to poll for the move's status.

        Note: moves will show as transactions, but not as transfers.

        This endpoint is in BETA, behaviour and specification may change without
        any previous notice.

        Permissions required: <code>MP_None_Write</code>

        :param amount: Amount to transfer. Must be positive.
        :type amount: float
        :param credit_account_id: The account to credit the funds to.
        :type credit_account_id: int
        :param debit_account_id: The account to debit the funds from.
        :type debit_account_id: int
        :param client_move_id: Client move ID.
                               May only contain alphanumeric (0-9, a-z, or A-Z) and special characters (_ ; , . -). Maximum length: 255.
                               It will be available in read endpoints, so you can use it to avoid duplicate moves between the same accounts.
                               Values must be unique across all your successful calls of this endpoint; trying to create a move request
                               with the same `client_move_id` as one of your past move requests will result in a HTTP 409 Conflict response.
        :type client_move_id: str
        """
        req = {
            'amount': amount,
            'credit_account_id': credit_account_id,
            'debit_account_id': debit_account_id,
            'client_move_id': client_move_id,
        }
        return self.do('POST', '/api/exchange/1/move', req=req, auth=True)

    def post_limit_order(self, pair, price, type, volume, base_account_id=None, client_order_id=None, counter_account_id=None, post_only=None, stop_direction=None, stop_price=None, timestamp=None, ttl=None):
        """Makes a call to POST /api/1/postorder.

        <b>Warning!</b> Orders cannot be reversed once they have executed.
        Please ensure your program has been thoroughly tested before submitting Orders.

        If no <code>base_account_id</code> or <code>counter_account_id</code> are specified,
        your default base currency or counter currency account will be used.
        You can find your Account IDs by calling the <a href="#operation/getBalances">Balances</a> API.

        Permissions required: <code>Perm_W_Orders</code>

        :param pair: The currency pair to trade.
        :type pair: str
        :param price: Limit price as a decimal string in units of ZAR/BTC.
        :type price: float
        :param type: <code>BID</code> for a bid (buy) limit order<br>
                     <code>ASK</code> for an ask (sell) limit order
        :type type: str
        :param volume: Amount of cryptocurrency to buy or sell as a decimal string in units of the currency.
        :type volume: float
        :param base_account_id: The base currency Account to use in the trade.
        :type base_account_id: int
        :param client_order_id: Client order ID.
                                May only contain alphanumeric (0-9, a-z, or A-Z) and special characters (_ ; , . -). Maximum length: 255.
                                It will be available in read endpoints, so you can use it to reconcile Luno with your internal system.
                                Values must be unique across all your successful order creation endpoint calls; trying to create an order
                                with the same `client_order_id` as one of your past orders will result in a HTTP 409 Conflict response.
        :type client_order_id: str
        :param counter_account_id: The counter currency Account to use in the trade.
        :type counter_account_id: int
        :param post_only: Post-only Orders will be cancelled if they would otherwise have traded
                          immediately.
                          For example, if there's a bid at ZAR 100,000 and you place a post-only ask at ZAR 100,000,
                          your order will be cancelled instead of trading.
                          If the best bid is ZAR 100,000 and you place a post-only ask at ZAR 101,000,
                          your order won't trade but will go into the order book.
        :type post_only: bool
        :param stop_direction: Side of the trigger price to activate the order. This should be set if `stop_price` is also
                               set.

                               `RELATIVE_LAST_TRADE` will automatically infer the direction based on the last
                               trade price and the stop price. If last trade price is less than stop price then stop
                               direction is ABOVE otherwise is BELOW.
        :type stop_direction: str
        :param stop_price: Trigger trade price to activate this order as a decimal string. If this
                           is set then this is treated as a Stop Limit Order and `stop_direction`
                           is expected to be set too.
        :type stop_price: float
        :param timestamp: Unix timestamp in milliseconds of when the request was created and sent.
        :type timestamp: int
        :param ttl: Specifies the number of milliseconds after timestamp the request is valid for.
                    If `timestamp` is not specified, `ttl` will not be used.
        :type ttl: int
        """
        req = {
            'pair': pair,
            'price': price,
            'type': type,
            'volume': volume,
            'base_account_id': base_account_id,
            'client_order_id': client_order_id,
            'counter_account_id': counter_account_id,
            'post_only': post_only,
            'stop_direction': stop_direction,
            'stop_price': stop_price,
            'timestamp': timestamp,
            'ttl': ttl,
        }
        return self.do('POST', '/api/1/postorder', req=req, auth=True)

    def post_market_order(self, pair, type, base_account_id=None, base_volume=None, client_order_id=None, counter_account_id=None, counter_volume=None, timestamp=None, ttl=None):
        """Makes a call to POST /api/1/marketorder.

        A Market Order executes immediately, and either buys as much of the asset that can be bought for a set amount of fiat currency, or sells a set amount of the asset for as much as possible.

        <b>Warning!</b> Orders cannot be reversed once they have executed.
        Please ensure your program has been thoroughly tested before submitting Orders.

        If no <code>base_account_id</code> or <code>counter_account_id</code> are specified, the default base currency or counter currency account will be used.
        Users can find their account IDs by calling the <a href="#operation/getBalances">Balances</a> request.

        Permissions required: <code>Perm_W_Orders</code>

        :param pair: The currency pair to trade.
        :type pair: str
        :param type: <code>BUY</code> to buy an asset<br>
                     <code>SELL</code> to sell an asset
        :type type: str
        :param base_account_id: The base currency account to use in the trade.
        :type base_account_id: int
        :param base_volume: For a <code>SELL</code> order: amount of the base currency to use (e.g. how much BTC to sell for EUR in the BTC/EUR market)
        :type base_volume: float
        :param client_order_id: Client order ID.
                                May only contain alphanumeric (0-9, a-z, or A-Z) and special characters (_ ; , . -). Maximum length: 255.
                                It will be available in read endpoints, so you can use it to reconcile Luno with your internal system.
                                Values must be unique across all your successful order creation endpoint calls; trying to create an order
                                with the same `client_order_id` as one of your past orders will result in a HTTP 409 Conflict response.
        :type client_order_id: str
        :param counter_account_id: The counter currency account to use in the trade.
        :type counter_account_id: int
        :param counter_volume: For a <code>BUY</code> order: amount of the counter currency to use (e.g. how much EUR to use to buy BTC in the BTC/EUR market)
        :type counter_volume: float
        :param timestamp: Unix timestamp in milliseconds of when the request was created and sent.
        :type timestamp: int
        :param ttl: Specifies the number of milliseconds after timestamp the request is valid for.
                    If `timestamp` is not specified, `ttl` will not be used.
        :type ttl: int
        """
        req = {
            'pair': pair,
            'type': type,
            'base_account_id': base_account_id,
            'base_volume': base_volume,
            'client_order_id': client_order_id,
            'counter_account_id': counter_account_id,
            'counter_volume': counter_volume,
            'timestamp': timestamp,
            'ttl': ttl,
        }
        return self.do('POST', '/api/1/marketorder', req=req, auth=True)

    def send(self, address, amount, currency, description=None, destination_tag=None, external_id=None, has_destination_tag=None, message=None):
        """Makes a call to POST /api/1/send.

        Send assets from an Account. Please note that the asset type sent must match the receive address of the same cryptocurrency of the same type - Bitcoin to Bitcoin, Ethereum to Ethereum, etc.

        Sends can be to a cryptocurrency receive address, or the email address of another Luno platform user.

        <b>Note:</b> This is currently unavailable to users who are verified in countries with money travel rules.

        Permissions required: <code>Perm_W_Send</code>

        :param address: Destination address or email address.

                        <b>Note</b>:
                        <ul>
                        <li>Ethereum addresses must be
                        <a href="https://github.com/ethereum/EIPs/blob/master/EIPS/eip-55.md" target="_blank" rel="nofollow">checksummed</a>.</li>
                        <li>Ethereum sends to email addresses are not supported.</li>
                        </ul>
        :type address: str
        :param amount: Amount to send as a decimal string.
        :type amount: float
        :param currency: Currency to send.
        :type currency: str
        :param description: User description for the transaction to record on the account statement.
        :type description: str
        :param destination_tag: Optional XRP destination tag. Note that HasDestinationTag must be true if this value is provided.
        :type destination_tag: int
        :param external_id: Optional unique ID to associate with this withdrawal.
                            Useful to prevent duplicate sends in case of failure.
                            This supports all alphanumeric characters, as well as "-" and "_".
        :type external_id: str
        :param has_destination_tag: Optional boolean flag indicating that a XRP destination tag is provided (even if zero).
        :type has_destination_tag: bool
        :param message: Message to send to the recipient.
                        This is only relevant when sending to an email address.
        :type message: str
        """
        req = {
            'address': address,
            'amount': amount,
            'currency': currency,
            'description': description,
            'destination_tag': destination_tag,
            'external_id': external_id,
            'has_destination_tag': has_destination_tag,
            'message': message,
        }
        return self.do('POST', '/api/1/send', req=req, auth=True)

    def send_fee(self, address, amount, currency):
        """Makes a call to GET /api/1/send_fee.

        Calculate fees involved with a crypto send request.

        Send address can be to a cryptocurrency receive address, or the email address of another Luno platform user.

        Permissions required: <code>MP_None</code>

        :param address: Destination address or email address.

                        <b>Note</b>:
                        <ul>
                        <li>Ethereum addresses must be
                        <a href="https://github.com/ethereum/EIPs/blob/master/EIPS/eip-55.md" target="_blank" rel="nofollow">checksummed</a>.</li>
                        <li>Ethereum sends to email addresses are not supported.</li>
                        </ul>
        :type address: str
        :param amount: Amount to send as a decimal string.
        :type amount: float
        :param currency: Currency to send.
        :type currency: str
        """
        req = {
            'address': address,
            'amount': amount,
            'currency': currency,
        }
        return self.do('GET', '/api/1/send_fee', req=req, auth=True)

    def stop_order(self, order_id):
        """Makes a call to POST /api/1/stoporder.

        Request to cancel an Order.

        <b>Note!</b>: Once an Order has been completed, it can not be reversed.
        The return value from this request will indicate if the Stop request was successful or not.

        Permissions required: <code>Perm_W_Orders</code>

        :param order_id: The Order identifier as a string.
        :type order_id: str
        """
        req = {
            'order_id': order_id,
        }
        return self.do('POST', '/api/1/stoporder', req=req, auth=True)

    def update_account_name(self, id, name):
        """Makes a call to PUT /api/1/accounts/{id}/name.

        Update the name of an account with a given ID.

        Permissions required: <code>Perm_W_Addresses</code>

        :param id: Account ID - the unique identifier for the specific Account.
        :type id: int
        :param name: The label to use for this account
        :type name: str
        """
        req = {
            'id': id,
            'name': name,
        }
        return self.do('PUT', '/api/1/accounts/{id}/name', req=req, auth=True)


# vi: ft=python
