
import pandas as pd
import json
import tt_dataManager
from datetime import datetime
import io
import os

print(datetime.now().strftime("%H:%M:%S"))

def create_dataframe(stockDict):
    
    # Initialize empty lists to store data
    ticker_list = []
    stockname_list = []
    exchange_list = []
    ipoDate_list = []
    status_list = []
    opens_list = []
    highs_list = []
    lows_list = []
    closes_list = []
    volumes_list = []

    # Iterate through each stock object
    for ticker, stock_obj in stockDict.items():
        # Append data to respective lists
        ticker_list.append(stock_obj.getTicker())
        stockname_list.append(stock_obj.getName())
        exchange_list.append(stock_obj.getExchange())
        ipoDate_list.append(stock_obj.getIpoDate())
        status_list.append(stock_obj.getStatus())
        # Convert JSON strings back to dictionaries
        opens_list.append(json.loads(stock_obj.getOpens()))
        highs_list.append(json.loads(stock_obj.getHighs()))
        lows_list.append(json.loads(stock_obj.getLows()))
        closes_list.append(json.loads(stock_obj.getCloses()))
        volumes_list.append(json.loads(stock_obj.getVolumes()))

    # Create a dictionary from the lists
    data = {
        'Ticker': ticker_list,
        'Stock Name': stockname_list,
        'Exchange': exchange_list,
        'IPO Date': ipoDate_list,
        'Status': status_list,
        'Opens': opens_list,
        'Highs': highs_list,
        'Lows': lows_list,
        'Closes': closes_list,
        'Volumes': volumes_list
    }

    # Create a DataFrame from the dictionary
    df = pd.DataFrame(data)
    
    return df

# Assuming you have a stockDict loaded from your JSON file
stockDict = tt_dataManager.loadStocks()

# Create DataFrame
df = create_dataframe(stockDict)

csv_file_path = 'data/DataFrame.csv'
df.to_csv(csv_file_path, index=False)

print(df)

print(datetime.now().strftime("%H:%M:%S"))
