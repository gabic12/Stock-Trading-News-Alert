import requests
import datetime as dt

STOCK_SYMBOL = "NVDA" #Change stock name here
COMPANY_NAME = "Nvidia" #Change company name here
STOCK_API_KEY = "Your Stock Price API Key"
NEWS_API_KEY = "Your News API Key"

#Date variables
today_date = dt.datetime.now().date()

#Stock market is closed on weekends, retrieve data from the last two trading days
if today_date.weekday() == 6: #Check if today is Sunday
    yesterday_date = str((dt.datetime.now() - dt.timedelta(2)).date()) #Friday
    two_days_ago_date = str((dt.datetime.now() - dt.timedelta(3)).date())  #Thursday
elif today_date.weekday() == 0: #Check if today is Monday
    yesterday_date = str((dt.datetime.now() - dt.timedelta(3)).date()) #Friday
    two_days_ago_date = str((dt.datetime.now() - dt.timedelta(4)).date()) #Thursday
elif today_date.weekday() == 1: #Check if today is Tuesday
    yesterday_date = str((dt.datetime.now() - dt.timedelta(1)).date()) #Monday
    two_days_ago_date = str((dt.datetime.now() - dt.timedelta(4)).date()) #Friday
else:
    yesterday_date = str((dt.datetime.now() - dt.timedelta(1)).date())
    two_days_ago_date = str((dt.datetime.now() - dt.timedelta(2)).date())

def get_stock_data():
    """Calls the Stock Price API and returns the percent difference between last two trading days closing price"""
    stock_api_parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK_SYMBOL,
        "apikey": STOCK_API_KEY
    }

    stock_response = requests.get(url="https://www.alphavantage.co/query)", params=stock_api_parameters)
    stock_response.raise_for_status()
    stock_data = stock_response.json()

    yesterday_close_price = float(stock_data["Time Series (Daily)"][yesterday_date]["4. close"])
    two_days_ago_close_price = float(stock_data["Time Series (Daily)"][two_days_ago_date]["4. close"])
    difference = yesterday_close_price - two_days_ago_close_price
    difference_percent = round(((difference / yesterday_close_price) * 100), 2)

    return difference_percent

def get_news_data():
    """Calls the News API and returns a list composed of the most 3 recent news articles"""
    news_api_parameters = {
        "qInTitle": COMPANY_NAME,
        "from": yesterday_date,
        "to": str(today_date),
        "sortBy": "popularity",
        "language": "en",
        "apiKey": NEWS_API_KEY
    }
    news_response = requests.get(url="https://newsapi.org/v2/everything", params=news_api_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"][:3]
    tree_articles =[f"Source: {news['source']['name']} \nAuthor: {news['author']} \nTitle: {news['title']} \nDescription: {news['description']}" for news in news_data]

    return tree_articles

percent = get_stock_data()
articles = get_news_data()

if percent >= 0:
    print(f"{STOCK_SYMBOL}: +{percent}% \n")
else:
    print(f"{STOCK_SYMBOL}: {percent}% \n")
    
for article in articles:
    print(article + "\n")
