import json

class myStock:
    __ticker = ""
    __stockname = ""
    __exchange = ""
    __assetType = ""
    __ipoDate = ""
    __status = ""
    __dates = []
    __opens = {}
    __highs = {}
    __lows = {}
    __closes = {}
    __adjustedCloses = {}
    __volumes = {}
    __dividends = {}
    __splitCoefficient = {}
    sharpe = ""
    ep = ""
    
    def __init__(self, ticker, stockname, exchange, assetType, ipoDate, status, opens=None, highs=None, lows=None, closes=None, adjustedCloses=None, volumes=None):
        self.__ticker = ticker
        self.__stockname = stockname
        self.__exchange = exchange
        self.__assetType = assetType
        self.__ipoDate = ipoDate
        self.__status = status
        self.__opens = opens if opens is not None else {}
        self.__highs = highs if highs is not None else {}
        self.__lows = lows if lows is not None else {}
        self.__closes = closes if closes is not None else {}
        self.__adjustedCloses = adjustedCloses if adjustedCloses is not None else {}
        self.__volumes = volumes if volumes is not None else {}

       
    
    def getTicker(self):
        return json.dumps(self.__ticker)
    
    def getName(self):
        return json.dumps(self.__stockname)
    
    def getExchange(self):
        return json.dumps(self.__exchange)
    
    def getAssetType(self):
        return json.dumps(self.__assetType)
    
    def getIpoDate(self):
        return json.dumps(self.__ipoDate)
    
    def getStatus(self):
        return json.dumps(self.__status)
    
    def setName(self, newName):
        self.__stockname = newName
    
    def print(self):
        print("===============")
        print(f"TICKER: {self.__ticker}")
        print(f"NAME: {self.__stockname}")
        print(f"EXCHANGE: {self.__exchange}")
        print(f"TYPE: {self.__assetType}")
        print(f"IPO DATE: {self.__ipoDate}")
        print(f"STATUS: {self.__status}")
        print("===============")

    def toJson(self):
        # Create a dictionary representation of the object
        json_data = {
        
            "ticker": self.__ticker,
            "stockname": self.__stockname,
            "exchange": self.__exchange,
            "assetType": self.__assetType,
            "ipoDate": self.__ipoDate,
            "status": self.__status,
            "opens": self.__opens,
            "highs": self.__highs,
            "lows": self.__lows,
            "adjustedCloses": self.__adjustedCloses,
            "volumes": self.__volumes,
        }
        # Serialize the dictionary to JSON string
        return json.dumps(json_data)
    


    def updateOHLCV(self, response):
        # Parse the JSON response into a dictionary
        OHLCVDat = json.loads(response.text)
        # Access the 'Time Series (Daily)' data
        time_series = OHLCVDat.get('Time Series (Daily)', {})

        # Iterate over each date in the time series
        for date, data in time_series.items():
            # Extract the "open" value for the current date
            open_value = data.get('1. open')
            
            if open_value is not None:
                # Convert the open value to float and append to self.__opens
                self.__opens.update({date:float(open_value)})
                #populates dates accordingly
                self.__dates.append(date)
            
                # Print the latest open value added to self.__opens
                #print(f"Added open value for {self.getTicker()} on {date}: {open_value}")
            else:
                self.__opens.update({date:"null"})
                # Handle missing "open" value for the current date
                #print(f"Warning: 'open' value missing for {self.getTicker()} on {date}")

        # Iterate over each date in the time series
        for date, data in time_series.items():
            # Extract the "high" value for the current date
            high_value = data.get('2. high')
            
            if high_value is not None:
                # Convert the high value to float and append to self.__opens
                self.__highs.update({date:float(high_value)})
            
                # Print the latest high value added to self.__opens
                #print(f"Added high value for {date}: {high_value}")
            else:
                self.__highs.update({date:"null"})
                # Handle missing "high" value for the current date
                #print(f"Warning: 'high' value missing for {date}")

        # Iterate over each date in the time series
        for date, data in time_series.items():
            # Extract the "open" value for the current date
            low_value = data.get('3. low')
            
            if low_value is not None:
                # Convert the low value to float and append to self.__opens
                self.__lows.update({date:float(low_value)})
            
                # Print the latest low value added to self.__opens
                #print(f"Added low value for {date}: {low_value}")
            else:
                self.__lows.update({date:"null"})
                # Handle missing "low" value for the current date
                #print(f"Warning: 'low' value missing for {date}")
        
        for date, data in time_series.items():
            # Extract the "close" value for the current date
            close_value = data.get('4. close')

            if close_value is not None:
                # Convert the close value to float and append to self.__opens
                self.__closes.update({date:float(close_value)})
                #populates dates accordingly
            
                # Print the latest close value added to self.__opens
                #print(f"Added close value for {date}: {close_value}")
            else:
                self.__closes.update({date:"null"})
                # Handle missing "close" value for the current date
                #print(f"Warning: 'close' value missing for {date}")

        for date, data in time_series.items():

            adjustedClose_value = data.get('5. adjusted close')

            if adjustedClose_value is not None:
                self.__adjustedCloses.update({date:float(adjustedClose_value)})
            else:
                self.__adjustedCloses.update({date:"null"})

        for date, data in time_series.items():

            volume_value = data.get('6. volume')

            if volume_value is not None:
                self.__volumes.update({date:float(volume_value)})
            else:
                self.__volumes.update({date:"null"})

        for date, data in time_series.items():

            dividend_value = data.get('7. dividend amount')

            if dividend_value is not None:
                self.__dividends.update({date:float(dividend_value)})
            else:
                self.__dividends.update({date:"null"})

        for date, data in time_series.items():

            splitCoefficient_value = data.get('8. split coefficient')

            if splitCoefficient_value is not None:
                self.__splitCoefficient.update({date:float(splitCoefficient_value)})
            else:
                self.__splitCoefficient.update({date:"null"})

    def getDates(self):
        return json.dumps(self.__dates)
    
    def getOpens(self):
        return json.dumps(self.__opens)
    
    def getHighs(self):
        return json.dumps(self.__highs)
    
    def getLows(self):
        return json.dumps(self.__lows)
    
    def getCloses(self):
        return json.dumps(self.__adjustedCloses)
    
    def getVolumes(self):
        return json.dumps(self.__volumes)

"""
        with open(tt_api.get_OHLCV()) as f:
            for jsonObj in f:
                stockDict = json.loads(jsonObj)
                OHLCVDat.append(stockDict)
        for date in OHLCVDat:
            print("================")
            print(f"Date: {self.__date}")
            print(f"Ticker: {self.__ticker}")
            print(f"Open: {self.__open}")
            print(f"High: {self.__high}")
            print(f"Low: {self.__low}")
            print(f"Close: {self.__close}")
            print(f"Adjusted Close: {self.__adjustedClose}")
            print(f"Volume: {self.__volume}")
            print(f"Dividends: {self.__dividends}")
            print(f"Split Coefficient: {self.__splitCoefficient}")
            print("================")
 """       
        
        
       
        #create the lists that contain all the OHLCV data