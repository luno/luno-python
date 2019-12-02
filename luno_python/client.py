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

        Cancel a withdrawal request. This can only be done if the request is still
        in state <code>PENDING</code>.

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

    def create_quote(self, type, base_amount, pair, base_account_id=None, counter_account_id=None):
        """Makes a call to POST /api/1/quotes.

        Creates a new quote to buy or sell a particular amount.

        You can specify either the exact amount that you want to pay or the exact
        amount that you want too receive.

        For example, to buy exactly 0.1 Bitcoin using ZAR, you would create a quote
        to BUY 0.1 XBTZAR. The returned quote includes the appropriate ZAR amount. To
        buy Bitcoin using exactly ZAR 100, you would create a quote to SELL 100
        ZARXBT. The returned quote specifies the Bitcoin as the counter amount that
        will be returned.

        An error is returned if your account is not verified for the currency pair,
        or if your account would have insufficient balance to ever exercise the
        quote.

        Permissions required: <code>Perm_W_Orders</code>

        :param type: <code>BUY</code> or <code>SELL</code>.
        :type type: str
        :param base_amount: Amount to buy or sell in the pair base currency.
        :type base_amount: float
        :param pair: Currency pair to trade. The pair can also be flipped if you want to buy
                     or sell the counter currency (e.g. ZARXBT).
        :type pair: str
        :param base_account_id: Optional account for the pair's base currency.
        :type base_account_id: int
        :param counter_account_id: Optional account for the pair's counter currency.
        :type counter_account_id: int
        """
        req = {
            'type': type,
            'base_amount': base_amount,
            'pair': pair,
            'base_account_id': base_account_id,
            'counter_account_id': counter_account_id,
        }
        return self.do('POST', '/api/1/quotes', req=req, auth=True)

    def create_withdrawal(self, type, amount, beneficiary_id=None, reference=None, external_id=None):
        """Makes a call to POST /api/1/withdrawals.

        Creates a new withdrawal request.

        Permissions required: <code>Perm_W_Withdrawals</code>

        :param type: Withdrawal type.
        :type type: str
        :param amount: Amount to withdraw. The currency depends on the type.
        :type amount: float
        :param beneficiary_id: The beneficiary ID of the bank account the withdrawal will be paid out
                               to. This parameter is required if you have multiple bank accounts. Your
                               bank account beneficiary ID can be found by clicking on the beneficiary
                               name on the <a href="/wallet/beneficiaries">Beneficiaries</a> page.
        :type beneficiary_id: int
        :param reference: For internal use.
        :type reference: str
        :param external_id: Optional unique ID to associate with this withdrawal. Useful to prevent
                            duplicate sends in case of failure. It supports all alphanumeric
                            characters, as well as "-" and "_".
        :type external_id: str
        """
        req = {
            'type': type,
            'amount': amount,
            'beneficiary_id': beneficiary_id,
            'reference': reference,
            'external_id': external_id,
        }
        return self.do('POST', '/api/1/withdrawals', req=req, auth=True)

    def discard_quote(self, id):
        """Makes a call to DELETE /api/1/quotes/{id}.

        Discard a quote. Once a quote has been discarded, it cannot be exercised even
        if it has not expired yet.

        Permissions required: <code>Perm_W_Orders</code>

        :param id: ID of the quote to discard.
        :type id: int
        """
        req = {
            'id': id,
        }
        return self.do('DELETE', '/api/1/quotes/{id}', req=req, auth=True)

    def exercise_quote(self, id):
        """Makes a call to PUT /api/1/quotes/{id}.

        Exercise a quote to perform the trade. If there is sufficient balance
        available in your account, it will be debited and the counter amount
        credited.

        An error is returned if the quote has expired or if you have insufficient
        available balance.

        Permissions required: <code>Perm_W_Orders</code>

        :param id: ID of the quote to exercise.
        :type id: int
        """
        req = {
            'id': id,
        }
        return self.do('PUT', '/api/1/quotes/{id}', req=req, auth=True)

    def get_balances(self, assets=None):
        """Makes a call to GET /api/1/balance.

        The list of all Accounts and their respective balances for the requesting user.

        Permissions required: <code>Perm_R_Balance</code>

        :param assets: Only return balances for wallets with these currencies (if not provided,
                       all balances will be returned)
        :type assets: list
        """
        req = {
            'assets': assets,
        }
        return self.do('GET', '/api/1/balance', req=req, auth=True)

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

    def get_lightning_receive(self, id):
        """Makes a call to GET /api/1/lightning/receive/{id}.

        <b>Alpha warning!</b> The Lightning API is still in Alpha stage.
        The risks are limited api availability and channel capacity.

        Lookup the status of a Lightning Receive Invoice.

        Permissions required: <code>Perm_W_Send</code>

        :param id: ID of invoice.
        :type id: int
        """
        req = {
            'id': id,
        }
        return self.do('GET', '/api/1/lightning/receive/{id}', req=req, auth=True)

    def get_order(self, id):
        """Makes a call to GET /api/1/orders/{id}.

        Get an order by its ID.

        Permissions required: <code>Perm_R_Orders</code>

        :param id: The order ID.
        :type id: str
        """
        req = {
            'id': id,
        }
        return self.do('GET', '/api/1/orders/{id}', req=req, auth=True)

    def get_order_book(self, pair):
        """Makes a call to GET /api/1/orderbook_top.

        Returns a list of the top 100 <em>bids</em> and <em>asks</em> for the currency pair specified in the Order Book.

        Ask Orders are sorted by price ascending.

        Bid Orders are sorted by price descending.

        Orders of the same price are aggregated.

        :param pair: Currency pair of the Orders to retrieve
        :type pair: str
        """
        req = {
            'pair': pair,
        }
        return self.do('GET', '/api/1/orderbook_top', req=req, auth=False)

    def get_order_book_full(self, pair):
        """Makes a call to GET /api/1/orderbook.

        This request returns a list of all <em>bids</em> and <em>asks</em> for the currency pair specified in the Order Book.

        Ask orders are sorted by price ascending.

        Bid orders are sorted by price descending.

        Multiple orders at the same price are not aggregated.

        <b>Warning:</b> This may return a large amount of data.
        Users are recommended to use the <a href="#operation/getOrderBook">top 100 bids and asks</a>
        or the <a href="#tag/streaming-API-(beta)">Streaming API</a>.

        :param pair: Currency pair of the Orders to retrieve
        :type pair: str
        """
        req = {
            'pair': pair,
        }
        return self.do('GET', '/api/1/orderbook', req=req, auth=False)

    def get_quote(self, id):
        """Makes a call to GET /api/1/quotes/{id}.

        Get the latest status of a quote.

        Permissions required: <code>Perm_R_Orders</code>

        :param id: ID of the quote to retrieve.
        :type id: int
        """
        req = {
            'id': id,
        }
        return self.do('GET', '/api/1/quotes/{id}', req=req, auth=True)

    def get_ticker(self, pair):
        """Makes a call to GET /api/1/ticker.

        Returns the latest ticker indicators.

        :param pair: Currency pair
        :type pair: str
        """
        req = {
            'pair': pair,
        }
        return self.do('GET', '/api/1/ticker', req=req, auth=False)

    def get_tickers(self):
        """Makes a call to GET /api/1/tickers.

        Returns the latest ticker indicators from all active Luno exchanges.

        """
        return self.do('GET', '/api/1/tickers', req=None, auth=False)

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

    def list_orders(self, state=None, pair=None, created_before=None, limit=None):
        """Makes a call to GET /api/1/listorders.

        Returns a list of the most recently placed Orders.
        Users can specify an optional <code>state=PENDING</code> parameter to restrict the results to only open Orders.
        Users can also specify the market by using the optional currency pair parameter.
        The list is truncated after 100 items.

        Permissions required: <code>Perm_R_Orders</code>

        :param state: Filter to only orders of this state
        :type state: str
        :param pair: Filter to only orders of this currency pair
        :type pair: str
        :param created_before: Filter to orders created before this timestamp (Unix milliseconds)
        :type created_before: int
        :param limit: Limit to this many orders
        :type limit: int
        """
        req = {
            'state': state,
            'pair': pair,
            'created_before': created_before,
            'limit': limit,
        }
        return self.do('GET', '/api/1/listorders', req=req, auth=True)

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

        Returns a list of the most recent trades that happened in the last 24h. At
        most 100 results are returned per call.

        :param pair: Currency pair
        :type pair: str
        :param since: Fetch trades executed after this time, specified as a Unix timestamp in
                      milliseconds.
        :type since: int
        """
        req = {
            'pair': pair,
            'since': since,
        }
        return self.do('GET', '/api/1/trades', req=req, auth=False)

    def list_transactions(self, id, min_row, max_row):
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
        :param min_row: Minimum of the row range to return (inclusive)
        :type min_row: int
        :param max_row: Maximum of the row range to return (exclusive)
        :type max_row: int
        """
        req = {
            'id': id,
            'min_row': min_row,
            'max_row': max_row,
        }
        return self.do('GET', '/api/1/accounts/{id}/transactions', req=req, auth=True)

    def list_user_trades(self, pair, since=None, before=None, after_seq=None, before_seq=None, sort_desc=None, limit=None):
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
        :param since: Filter to trades on or after this timestamp.
        :type since: int
        :param before: Filter to trades before this timestamp.
        :type before: int
        :param after_seq: Filter to trades from (including) this sequence number.
                          Default behaviour is not to include this filter.
        :type after_seq: int
        :param before_seq: Filter to trades before (excluding) this sequence number.
                           Default behaviour is not to include this filter.
        :type before_seq: int
        :param sort_desc: If set to true, sorts trades in descending order, otherwise ascending
                          order will be assumed.
        :type sort_desc: bool
        :param limit: Limit to this number of trades (default 100).
        :type limit: int
        """
        req = {
            'pair': pair,
            'since': since,
            'before': before,
            'after_seq': after_seq,
            'before_seq': before_seq,
            'sort_desc': sort_desc,
            'limit': limit,
        }
        return self.do('GET', '/api/1/listtrades', req=req, auth=True)

    def list_withdrawals(self):
        """Makes a call to GET /api/1/withdrawals.

        Returns a list of withdrawal requests.

        Permissions required: <code>Perm_R_Withdrawals</code>

        """
        return self.do('GET', '/api/1/withdrawals', req=None, auth=True)

    def post_limit_order(self, pair, type, post_only=None, volume, price, base_account_id=None, counter_account_id=None):
        """Makes a call to POST /api/1/postorder.

        Create a new trade order.

        Warning! Orders cannot be reversed once they have executed. Please ensure
        your program has been thoroughly tested before submitting orders.

        If no <code>base_account_id</code> or <code>counter_account_id</code> are
        specified, your default base currency or counter currency account will be
        used. You can find your account IDs by calling the
        <a href="#operation/getBalances">Balances</a> API.

        Permissions required: <code>Perm_W_Orders</code>

        :param pair: The currency pair to trade.
        :type pair: str
        :param type: <code>BID</code> for a bid (buy) limit order<br>
                     <code>ASK</code> for ab ask (sell) limit order
        :type type: str
        :param post_only: Post-only orders will be cancelled if they would otherwise have traded
                          immediately. For example, if there's a bid at ZAR 100,000 and you place
                          a post-only ask at ZAR 100,000, your order will be cancelled instead of
                          trading. If the best bid is ZAR 100,000 and you place a post-only ask at
                          ZAR 101,000, your order won't trade but will go into the order book.
        :type post_only: bool
        :param volume: Amount of Bitcoin or Ethereum to buy or sell as a decimal string in units
                       of the currency.
        :type volume: float
        :param price: Limit price as a decimal string in units of ZAR/BTC.
        :type price: float
        :param base_account_id: The base currency account to use in the trade.
        :type base_account_id: int
        :param counter_account_id: The counter currency account to use in the trade.
        :type counter_account_id: int
        """
        req = {
            'pair': pair,
            'type': type,
            'post_only': post_only,
            'volume': volume,
            'price': price,
            'base_account_id': base_account_id,
            'counter_account_id': counter_account_id,
        }
        return self.do('POST', '/api/1/postorder', req=req, auth=True)

    def post_market_order(self, pair, type, counter_volume=None, base_volume=None, base_account_id=None, counter_account_id=None):
        """Makes a call to POST /api/1/marketorder.

        Create a new Market Order.

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
        :param counter_volume: For a <code>BUY</code> order: amount of the counter currency to use (e.g. how much EUR to use to buy BTC in the BTC/EUR market)
        :type counter_volume: float
        :param base_volume: For a <code>SELL</code> order: amount of the base currency to use (e.g. how much BTC to sell for EUR in the BTC/EUR market)
        :type base_volume: float
        :param base_account_id: The base currency account to use in the trade.
        :type base_account_id: int
        :param counter_account_id: The counter currency account to use in the trade.
        :type counter_account_id: int
        """
        req = {
            'pair': pair,
            'type': type,
            'counter_volume': counter_volume,
            'base_volume': base_volume,
            'base_account_id': base_account_id,
            'counter_account_id': counter_account_id,
        }
        return self.do('POST', '/api/1/marketorder', req=req, auth=True)

    def receive_lightning(self, currency=None, amount, expires_at=None, description=None):
        """Makes a call to POST /api/1/lightning/receive.

        <b>Alpha warning!</b> The Lightning API is still in Alpha stage.
        The risks are limited api availability and channel capacity.

        Create a lightning invoice which can be used to receive
        BTC payments over the lightning network.

        Permissions required: <code>Perm_W_Send</code>

        :param currency: Currency to receive (defaults to XBT).
        :type currency: str
        :param amount: Amount to send as a decimal string.
        :type amount: float
        :param expires_at: Unix expiry timestamp (ms).

                           in query
        :type expires_at: int
        :param description: User defined description to add to lightning invoice.
        :type description: str
        """
        req = {
            'currency': currency,
            'amount': amount,
            'expires_at': expires_at,
            'description': description,
        }
        return self.do('POST', '/api/1/lightning/receive', req=req, auth=True)

    def send(self, amount, currency, address, description=None, message=None, external_id=None):
        """Makes a call to POST /api/1/send.

        Send Bitcoin from your account to a Bitcoin address or email address. Send
        Ethereum from your account to an Ethereum address.

        If the email address is not associated with an existing Luno account, an
        invitation to create an account and claim the funds will be sent.

        Warning! Cryptocurrency transactions are irreversible. Please ensure your
        program has been thoroughly tested before using this call.

        Permissions required: <code>Perm_W_Send</code>

        :param amount: Amount to send as a decimal string.
        :type amount: float
        :param currency: Currency to send.
        :type currency: str
        :param address: Destination Bitcoin address or email address, or Ethereum address to send
                        to.

                        Note:
                        <ul>
                        <li>Ethereum addresses must be
                        <a href="https://github.com/ethereum/EIPs/blob/master/EIPS/eip-55.md" target="_blank" rel="nofollow">checksummed</a>.</li>
                        <li>Ethereum sends to email addresses are not supported.</li>
                        </ul>
        :type address: str
        :param description: Description for the transaction to record on the account statement.
        :type description: str
        :param message: Message to send to the recipient. This is only relevant when sending to
                        an email address.
        :type message: str
        :param external_id: Optional unique ID to associate with this withdrawal. Useful to prevent
                            duplicate sends in case of failure. It supports all alphanumeric
                            characters, as well as "-" and "_".
        :type external_id: str
        """
        req = {
            'amount': amount,
            'currency': currency,
            'address': address,
            'description': description,
            'message': message,
            'external_id': external_id,
        }
        return self.do('POST', '/api/1/send', req=req, auth=True)

    def send_lightning(self, currency=None, payment_request, description=None, external_id=None):
        """Makes a call to POST /api/1/lightning/send.

        <b>Alpha warning!</b> The Lightning API is still in Alpha stage.
        The risks are limited api availability and channel capacity.

        Send Bitcoin over the Lightning network from your Bitcoin Account.

        Warning! Cryptocurrency transactions are irreversible. Please ensure your
        program has been thoroughly tested before using this call.

        Permissions required: <code>Perm_W_Send</code>

        :param currency: Currency to send.
        :type currency: str
        :param payment_request: Lightning payment request to send to.
        :type payment_request: str
        :param description: Description for the transaction to record on the account statement.
        :type description: str
        :param external_id: Optional unique ID to associate with this withdrawal. Useful to prevent
                            duplicate sends in case of failure. It supports all alphanumeric
                            characters, as well as "-" and "_".
        :type external_id: str
        """
        req = {
            'currency': currency,
            'payment_request': payment_request,
            'description': description,
            'external_id': external_id,
        }
        return self.do('POST', '/api/1/lightning/send', req=req, auth=True)

    def stop_order(self, order_id):
        """Makes a call to POST /api/1/stoporder.

        Request to stop an order.

        Permissions required: <code>Perm_W_Orders</code>

        :param order_id: The order reference as a string.
        :type order_id: str
        """
        req = {
            'order_id': order_id,
        }
        return self.do('POST', '/api/1/stoporder', req=req, auth=True)


# vi: ft=python
