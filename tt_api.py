import requests
import time
import tt_stockClass
import tt_dataManager
import os
import io
import numpy



def get_listing_status():
    base_url = "https://www.alphavantage.co/query"
    function = "LISTING_STATUS"
    key = "HGC6XVCK2JJ98QD1"

    # Construct the API request URL
    api_url = f"{base_url}?function={function}&apikey={key}"

    # Send the API request and get the response
    response = requests.get(api_url)

    # Check if the request was successful
    if response.status_code == 200:
        return response.text
    else:
        return None


def get_OHLCV(stockDict):

    base_url = "https://www.alphavantage.co/query"
    function = "TIME_SERIES_DAILY_ADJUSTED"
    key = "HGC6XVCK2JJ98QD1"

    timeoutCounter = 0

    for ticker, stock in stockDict.items():
        # Construct URL request
        api_url = f"{base_url}?function={function}&symbol={ticker}&outputsize=full&apikey={key}"

        while True:
            response = requests.get(api_url)
            
            # Check if the request was successful
            if response.status_code == 200:
                if len(response.text) > 0:
                    stockDict.get(ticker).updateOHLCV(response)
                    break
            else:
                return None

            # Wait before retrying
            time.sleep(2)
            timeoutCounter += 1

            # Check if timeoutCounter exceeds limit
            if timeoutCounter > 150:
                return "ERROR: AlphaVantage OHLCV TIMEOUT"
        
        # Reset the timeout counter after a successful request
        timeoutCounter = 0
        
    return stockDict



    

    

"""
    # Send request and ger response
    response = requests.get(api_url)
    
    # Check if request was successful if not wait and try else fail
    if response.status_code == 200 and len(response) > 0:
        return response.text
    elif response.status_code == 200 and len(response) == 0:
        print("running more pulls")
        time.sleep(90) #sleep program for the minute when data pulls run out

        return response.text #run url from stop point
    else:
        print("Something went wrong with OHLCV pull")
        return None

"""





#class otherAPI:
#  key = ""

# def init(self, key):
#     self.key = key