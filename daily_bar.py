

class DailyBar:
    def __init__(self, high, open, low, close, date, volume):
        self.high = high
        self.open = open
        self.low = low
        self.close = close
        self.date = date
        self.volume = volume

    def __str__(self):
        return f"Date: {self.date}, Open: {self.open}, High: {self.high}, Low: {self.low}, Close: {self.close}, Volume: {self.volume}"
