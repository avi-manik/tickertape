import tt_functions
import tt_stockClass
import tt_api
from tt_stockClass import myStock
import json
import io
import os
from datetime import datetime


#define function to create json file
def saveStocks(stockDict):

    with io.open(os.path.join("data/StockList.json"), "w") as db_file:
        total_keys = len(stockDict)
        #goes through every stock in list and collects json data
        db_file.write("[\n")
        for index, key in enumerate(stockDict):
            json_dict = {}
            if len(key) == 0:
                continue
            json_dict[index] = json.loads(stockDict[key].toJson())
            db_file.write(json.dumps(json_dict))
            if index < total_keys - 1:
                db_file.write(",\n") 
            #db_file.write("\\n"); look up how to do new lines .json
        db_file.write("\n]")
   
#print JSON
def loadStocks():
   # Opening JSON file
    with open(os.path.join("data/StockList.json"), "r") as f:
        # returns JSON object as a dictionary
        data = json.load(f)

    # Iterating through the json list
    stockDict = {}
    for stock_entry in data:
        for key, stock_data in stock_entry.items():  # Access the inner dictionary with key '0'
            stock_obj = tt_stockClass.myStock(
                stock_data.get('ticker', 'N/A'),  # Access keys safely with .get() method
                stock_data.get('stockname', 'N/A'),
                stock_data.get('exchange', 'N/A'),
                stock_data.get('assetType', 'N/A'),
                stock_data.get('ipoDate', 'N/A'),
                stock_data.get('status', 'N/A'),
                stock_data.get('opens', {}),
                stock_data.get('highs', {}),
                stock_data.get('lows', {}),
                stock_data.get('closes', {}),
                stock_data.get('adjustedCloses', {}),
                stock_data.get('volumes', {})
            )
            stockDict.update({stock_obj.getTicker(): stock_obj})
    return stockDict

def updateStocks():
    print(datetime.now().strftime("%H:%M:%S"))
    data = tt_api.get_listing_status()
    lines = data.split("\r\n")
    lines.remove(lines[0])
    tickerDict = {}
    #for line in lines[0:4]:
    #for line in lines[11500:-3]:
    for line in lines[:-3]:
        fields = line.split(",")
        newStock = myStock(fields[0], fields[1], fields[2], fields[3], fields[4], fields[6])
        tickerDict.update({fields[0]:newStock})
    tt_api.get_OHLCV(tickerDict)
    saveStocks(tickerDict)
    print(datetime.now().strftime("%H:%M:%S"))
    if len(tickerDict) == 0:
        return "no more api pulls :("
    

"""   
def loadOHLCV():
   f = open(os.path.join("data/StockList.json"))
   data = json.load(f)
    # Iterating through the json
    # list
   stockDict = {}
   for key in data:
        stock_data = data[key]
        stock_obj = tt_stockClass.myStock[
            stock_data['_myStock__dates'],
            stock_data['_myStock__opens'],
            stock_data['_myStock__highs'],
            stock_data['_myStock__lows'],
            stock_data['_myStock__closes'],
            stock_data['_myStock__adjustedCloses'],
            stock_data['_myStock__volumes'],
            stock_data['_myStock__dividends'],
            stock_data['_myStock__splitCoefficients']
        ]
        stockDict.update({[stock_obj.getDates]:stock_obj})
   return stockDict
"""
"""

def saveOHLCV(stockDict):
    with open ("data/StockList.json", "a") as db_file:
        openDict = {}
        for index, ticker in enumerate(openDict):
            openDict[index] = json.loads(openDict[ticker].toJson())
        db_file.write(json.dumps(openDict))


    for ticker, stock_obj in openDict.items():
        stock_data = ticker[stockDict]
        stock_obj = tt_stockClass.myStock(
            stock_data['_myStock__dates'],
            stock_data['_myStock__opens'],
        )
        openDict.update({
            stock_obj.getTicker():{
                [stock_obj.getDates()]:stock_obj
                }
        })
    return stockDict

"""



"""
    else:
      
        tickerDict = tt_api.get_OHLCV(tickerDict)
        saveStocks(tickerDict)
        print(tickerDict)
        print(datetime.now().strftime("%H:%M:%S"))
        return tickerDict
"""