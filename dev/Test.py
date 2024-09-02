""""
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt

ts = TimeSeries(key="HGC6XVCK2JJ98QD1", output_format="pandas")
extend_hours = False
data, meta_data = ts.get_intraday(symbol="IBM",interval="1min", outputsize="full")
print("index:", data.index)
print(data)
data["4. close"].plot()
plt.title("Intraday Times Series for the IBM stock (hour)")
plt.show()
"""
import os
import io
import tt_dataManager

open(os.path.join("tt_dataManager"))

tt_dataManager.showStockList()
