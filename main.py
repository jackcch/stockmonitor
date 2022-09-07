import requests
import os
from twilio.rest import Client

# Simple Python program demonstrating the usage of API to
# - Retrieve Stock Data via API from AlphaVantage.co
# - Get news via API from NewsAPI.org
# - Send SMS notifications via API through twilio

# CONSTANTS - Secrets are passed in from environment variables set in venv activate.ps1
STOCK = "LULU"
COMPANY_NAME = "LULULEMON"
STOCK_API_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = os.environ.get('STOCK_API_KEY')
NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
# SMS API
SID= os.environ.get('SMSSID')
AUTH_TOKEN=os.environ.get('SMSAUT')
VR_PHONE_NO=os.environ.get('SMSVRN')


direction_arrow=""
percentage_diff=0

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
    global direction_arrow, percentage_diff    
    t1_close = float(stockdata[0]['4. close'])
    t2_close = float(stockdata[1]['4. close'])
    diff = t1_close - t2_close
    diff_percentage = (diff / t1_close) * 100
    percentage_diff=diff_percentage
    if diff_percentage > 1 or diff_percentage < -1:
        direction_arrow="⬆️"
        return True
    else:
        direction_arrow="⬇️"
        return False    
    

def getnews():
    updatenews = ""
    news_head = {
        "Authorization": NEWS_API_KEY,
    }
    news_params = {
        "q": COMPANY_NAME,
        "language": "en",
        "pagesize": 3,
    }
    news_response = requests.get(url=NEWS_API_ENDPOINT, params=news_params, headers=news_head)
    news_response.raise_for_status
    print(news_response.status_code)
    news_data = news_response.json()
    print(news_data)
    news_data = news_response.json()['articles']
    for each in news_data:
        updatenews = updatenews + f"- {each['title']}\n"
    return updatenews


def sendSMS(parm_message):
    client = Client(SID, AUTH_TOKEN)
    message = client.messages.create(
        body=parm_message,
        from_=VR_PHONE_NO,
        to='+6597318207'
    )
    print(message.status)


# Main Program
dataset = checkstock()
if highstockmovement(dataset):
    latest_news = getnews()
    if latest_news != "":
        sms_message = f"{direction_arrow} {percentage_diff}\n{latest_news}"
        sendSMS(sms_message)
    else:
        print('No News Found')
else:
    print('No Activity')
