import pandas as pd
import yfinance as yf


class YahooFinanceClient(object):
    def __init__(self, company_symbol):
        self.company_symbol = company_symbol
        self.ticker = yf.Ticker(self.company_symbol)
        self.is_valid = False

    def validate_ticker(self):
        info = self.ticker.history(period='5d', interval='1d')
        self.is_valid = len(info) > 0

        return self.is_valid

    def historical_data(self, date_from, date_to):
        if not self.ticker:
            return pd.DataFrame()

        return yf.download(self.company_symbol, start=date_from, end=date_to)
