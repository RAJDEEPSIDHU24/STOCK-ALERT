import yfinance as yf
from datetime import datetime
import textwrap
import inspect

class StockChangeRecognizer():
    def __init__(self, stock_name: str, symbol: str, from_date: str, to_date: str):
        self.stock_name = stock_name
        self.symbol = symbol
        self.from_date = from_date
        self.to_date = to_date

        self._stock_message = ""
        self._big_delta = False
        self.price_ratio_percentage = None
        self.chart_data = None 

    def get_data_and_analyze(self):
        try:
            #  it will download stock data using yfinance
            data = yf.download(self.symbol, start=self.from_date, end=self.to_date, auto_adjust=True)

            #  To check if enough data is available for analysis
            if data.empty or data.shape[0] < 2:
                self._stock_message = f"⚠️ Not enough data for {self.stock_name} between {self.from_date} and {self.to_date}."
                self.chart_data = None # Ensure no chart data is returned
                return

            required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            
            missing_columns = [col for col in required_columns if col not in data.columns]
            if missing_columns:
                self._stock_message = f"❌ Error: Missing stock data columns for {self.stock_name}: {', '.join(missing_columns)}. Cannot perform full analysis or chart."
                self.chart_data = None
                return
            last_two = data.tail(2)

            if len(last_two) < 2:
                self._stock_message = f"⚠️ Not enough data for {self.stock_name} to compare last two days. Need at least two data points."
                self.chart_data = None
                return

            # Extract 'High' prices for yesterday and the day before yesterday
            # Using .item() to get the scalar value from a single-element Series to avoid FutureWarning
            price_yesterday = float(last_two.iloc[1]['High'].item())
            price_before_yesterday = float(last_two.iloc[0]['High'].item())

            #  if price_before_yesterday is 0 handle the problem
            if price_before_yesterday == 0:
                self._stock_message = f"❌ Error: Price before yesterday is zero for {self.stock_name}. Cannot calculate percentage change."
                self.chart_data = None
                return

            #  percentage change
            base_price_ratio = price_before_yesterday / 100
            self.price_ratio_percentage = (price_yesterday / base_price_ratio) - 100

            #  stock's change message based on the percentage
            if self.price_ratio_percentage <= -5.0:
                self._stock_message += f"\n🔴 {self.stock_name}: Decreased by ↘️ {round(self.price_ratio_percentage, 2)}%"
                self._big_delta = True
            elif self.price_ratio_percentage >= 5.0:
                self._stock_message += f"\n🟢 {self.stock_name}: Increased by ↗️ {round(self.price_ratio_percentage, 2)}%"
                self._big_delta = True
            else:
                self._stock_message += f"\n⚪ {self.stock_name}: Minor change {round(self.price_ratio_percentage, 2)}%"

            # Store the data needed for Plotly, ensuring each column is a Series before .tolist()
            
            self.chart_data = {
                'dates': data.index.strftime('%Y-%m-%d').tolist(), # Convert datetime index to string list
                'close': data['Close'].squeeze().tolist(),
                'open': data['Open'].squeeze().tolist(),
                'high': data['High'].squeeze().tolist(),
                'low': data['Low'].squeeze().tolist(),
                'volume': data['Volume'].squeeze().tolist()
            }

        except Exception as e:
           
            self._stock_message = f"❌ Error fetching data for {self.stock_name}: {str(e)}"
            self.chart_data = None #------------------ Ensure no chart data on error

    def get_message(self):
        # Get the current stock message
        msg = self._stock_message
        
        return textwrap.dedent(inspect.cleandoc(msg))

    @property
    def big_delta(self):
       
        return self._big_delta

