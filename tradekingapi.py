import os
import sys
import requests

from oauth_hook import OAuthHook


class TradeKingAPI(object):

    HOST = 'https://api.tradeking.com/v1'

    def __init__(self,
                 CK = os.environ.get('TK_CONSUMER_KEY'),
                 CS = os.environ.get('TK_CONSUMER_SECRET'),
                 OT = os.environ.get('TK_OAUTH_TOKEN'),
                 OS = os.environ.get('TK_OAUTH_SECRET'),
                 verbose = sys.stdout,
                 format  = 'json'):

        hook   = OAuthHook(OT, OS, CK, CS)
        config = dict(verbose = verbose)
        hooks  = dict(pre_request = hook)

        self.client = requests.session(config=config, hooks=hooks)
        self.format = format
#~------------------------------------------------------------------------------
#~Account Calls ----------------------------------------------------------------
    def accounts(self):
        '''This call will return detailed balance and holding information for each
        account associated with a user.'''
        url = '{0}/accounts.{1}'.format(self.HOST, self.format)
        return self.client.get(url)

    def accounts_balances(self):
        '''This call will return summary balance information for each account
        associated with a user as well as the total value for all accounts
        associated with a user.'''
        url = '{0}/accounts/balances.{1}'.format(self.HOST, self.format)
        return self.client.get(url)

    def accounts_id(self, id):
        '''This call will return detailed balance and holding information for the
        account number specified in the URI.'''
        url = '{0}/accounts/{1}.{2}'.format(self.HOST, id, self.format)
        return self.client.get(url)

    def accounts_id_balances(self, id):
        '''This call will return detailed balance information for the account
        number specified in the URI.'''
        url = '{0}/accounts/{1}/balances.{2}'.format(self.HOST, id, self.format)
        return self.client.get(url)

    def accounts_id_history(self, id, range='all', transactions='all'):
        '''This call will return account activity for the account number specified
        in the URI. This call supports optional date range or transaction type
        filters.

        range values: all, today, current_week, current_month, last_month
        transaction values: all, bookkeeping, trade
        '''
        url = '{0}/accounts/{1}/history.{2}'.format(self.HOST, id, self.format)
        data = dict(range=range, transactions=transactions)
        return self.client.get(url, data=data)

    def accounts_id_holdings(self, id):
        url = '{0}/accounts/{1}/holdings.{2}'.format(self.HOST, id, self.format)
        return self.client.get(url)
#~------------------------------------------------------------------------------
#~Trade Calls ------------------------------------------------------------------
    def accounts_id_orders(self, id, method='get', fixml=None):
        url = '{0}/accounts/{1}/orders{2}'.format(self.HOST, id, self.format)
        if method == 'get':
            return self.client.get(url)
        elif method == 'post':
            return self.client.post(url)
        else:
            raise "Invalid method {}".format(method)

    def accounts_id_orders_preview(self, id):
        url = '{0}/accounts/{1}/orders/preview.{2}'.format(self.HOST, id, self.format)
        return self.client.post(url)
#~------------------------------------------------------------------------------
#~Market Calls -----------------------------------------------------------------
    def market_clock(self):
        url = '{0}/market/clock.{1}'.format(self.HOST, self.format)
        return self.client.get(url)

    def market_ext_quotes(self, symbols, fids=None):
        url = '{0}/market/ext/quotes.{1}'.format(self.HOST, self.format)
        data = dict(symbols=symbols, fids=fids)
        return self.client.get(url, data=data)

    def market_historical_search(self, symbols, interval, startdate, enddate):
        url = '{0}/market/historical/search.{1}'.format(self.HOST, self.format)
        data = dict(symbols=symbols, interval=interval, startdate=startdate, enddate=enddate)
        return self.client.get(url, data=data)

    def market_news_search(self, keywords, startdate, enddate, symbols=None, maxhits=10):
        url = '{0}/market/news/search.{1}'.format(self.HOST, self.format)
        data = dict(keywords=keywords, symbols=symbols, maxhits=maxhits,
                    startdate=startdate, enddate=enddate)
        return self.client.get(url, data=data)

    def market_news_id(self, id):
        url = '{0}/market/news/{1}.{2}'.format(self.HOST, id, self.format)
        return self.client.get(url)

    def market_options_search(self):
        pass

    def market_options_strite(self):
        pass

    def market_options_expirations(self):
        pass

    def market_timesales(self):
        pass

    def market_toplists(self):
        pass
#~------------------------------------------------------------------------------
#~Member Calls -----------------------------------------------------------------
    def member_profile(self):
        url = '{0}/member/profile.{1}'.format(self.HOST, self.format)
        return self.client.get(url)
#~------------------------------------------------------------------------------
#~Utility Calls ----------------------------------------------------------------
    def utility_status(self):
        url = '{0}/utility/status.{1}'.format(self.HOST, self.format)
        return self.client.get(url)

    def utility_version(self):
        url = '{0}/utility/version.{1}'.format(self.HOST, self.format)
        return self.client.get(url)
#~------------------------------------------------------------------------------
#~Watchlist Calls --------------------------------------------------------------
    def watchlists(self, name=None, symbols=None, method='get'):
        url = '{0}/watchlist.{1}'.format(self.HOST, self.format)
        if method.lower() == 'post':
            if name is None:
                raise 'Need name for watchlist'
            elif symbols is None:
                raise 'Need symbols to POST'
            else:
                data = dict(symbols=symbols, id=name)
                return self.client.post(url, data=data)
        elif method.lower() == 'get':
            return self.client.post(url)
        else:
            raise 'Invalid method {}'.format(method)

    def watchlists_id(self, name, method='get'):
        url = '{0}/watchlists/{1}.{2}'.format(self.HOST, name, self.format)
        if method.lower() == 'get':
            return self.client.get(url)
        elif method.lower() == 'delete':
            return self.client.delete(url)
        else:
            raise 'Invalid method {}'.format(method)

    def watchlists_id_symbols(self, name, symbols, method='post'):
        '''
        [POST] - add the symbols in the form parameters to the watchlist
                 specified in the URI

        [DELETE] - delete the symbol in the URI for the watchlist specified in
                   the URI
        '''
        url = '{0}/watchlists/{1}/symbols.{2}'.format(self.HOST, name, self.format)
        if method.lower() == 'post':
            return self.client.get(url)
        elif method.lower() == 'delete':
            return self.client.delete(url)
        else:
            raise 'Invalid method {}'.format(method)
#~------------------------------------------------------------------------------


api = TradeKingAPI()

test = api.market_historical_search('goog', 'daily', '2012-01-10', '2013-01-20')


