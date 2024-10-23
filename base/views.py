from django.shortcuts import render
from django.views import View
import yfinance as yf

class Home(View):
    def get(self, request):
        ticker = request.GET.get('ticker', 'AAPL')  # Default to AAPL if no ticker is provided
        data = yf.Ticker(ticker)

        try:
            history = data.history(period="max")
            history = history.drop(columns=['Dividends', 'Stock Splits'])
            history.reset_index(inplace=True)
            history = history.tail(30).to_dict(orient="records")  # Latest 10 records

            # Fetch balance sheet data
            balance_sheet = data.balance_sheet
            balance_sheet.reset_index(inplace=True)
            balance_sheet = balance_sheet.to_dict(orient="records")  # Convert to dict for template

            context = {
                "ticker": ticker,
                "history": history,
                "balance_sheet": balance_sheet,
                "error_message": None
            }

        except KeyError:
            error_message = "The ticker symbol you entered is not valid. Please check the symbol and try again."
            context = {
                "history": [],
                "balance_sheet": [],
                "error_message": error_message
            }

        return render(request, 'base/home.html', context)

