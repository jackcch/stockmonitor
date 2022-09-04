import requests
import os

# Simple Python program demonstrating the usage of API to
# - Retrieve Stock Data via API from AlphaVantage.co
# - Get news via API from NewsAPI.org
# - Send SMS notifications via API through twilio

# CONSTANTS
STOCK = "LULU"
COMPANY_NAME = "LULULEMON"
STOCK_API_ENDPOINT = "https://www.alphavantage.co/query"
# STOCK_API_KEY = "71URQGF12S1WQ7L7"
STOCK_API_KEY = os.environ.get('STOCK_API_KEY')
NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything"
# NEWS_API_KEY = "beedff171ef247318131a992a2afc418"
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')

def checkstock():
    stock_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK,
        "apikey": STOCK_API_KEY,
    }
    response = requests.get(url=STOCK_API_ENDPOINT, params=stock_params)
    response.raise_for_status
    response_data = response.json()['Time Series (Daily)']
    data_list = [value for (key, value) in response_data.items()]
    return data_list
    
    
def highstockmovement(stockdata):
    t1_close = float(stockdata[0]['4. close'])
    t2_close = float(stockdata[1]['4. close'])
    diff = t1_close - t2_close
    diff_percentage = (diff / t1_close) * 100
    if diff_percentage > 5 or diff_percentage < -5:
        return True
    else:
        return False    
    

def getnews():
    updatenews = ""
    news_params = {
        "q": COMPANY_NAME,
        "language": "en",
        "pagesize": 3,
        "apiKey": NEWS_API_KEY,
    }
    news_response = requests.get(url=NEWS_API_ENDPOINT, params=news_params)
    news_response.raise_for_status
    news_data = news_response.json()['articles']
    for each in news_data:
        updatenews = updatenews + f"- {each['title']}\n"
    return updatenews


# Main Program
dataset = checkstock()
if highstockmovement(dataset):
    latest_news = getnews()
    print(latest_news)
else:
    print('No Activity')
