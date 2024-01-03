import requests
import os
from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()

TWILIO_API_KEY = os.getenv("T_API_KEY")
TWILIO_NUMBER = "+16814043516"
account_sid = "AC75458bc8be4f391631d06a145c19b148"
auth_token = os.getenv("T_AUTH_TOKEN")

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_API_KEY = os.getenv("STOCK_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}
stock = requests.get(STOCK_ENDPOINT, params=stock_parameters)
stock_data = stock.json()["Time Series (Daily)"]
data_list = [value for (key, value) in stock_data.items()]
yesterday_stock_price = float(data_list[0]["4. close"])

day_bef_yes = float(data_list[1]["4. close"])

stock_price_diff = abs(yesterday_stock_price - day_bef_yes)

diff_percentage = (stock_price_diff / float(yesterday_stock_price)) * 100

news_parameters = {
    "qInTitle": COMPANY_NAME,
    "apiKey": NEWS_API_KEY,
}

if diff_percentage > 5:
    news = requests.get(NEWS_ENDPOINT, params=news_parameters)
    articles = news.json()["articles"][:3]
    for article in articles:
        client = Client(account_sid, auth_token)
        if (yesterday_stock_price - day_bef_yes) > 0:
            message = client.messages \
                .create(
                    body=f"{STOCK_NAME}: 🔺{round(diff_percentage)}%\n\nHeadline: {article["title"]}\n\n"
                         f"Brief: {article["description"]}",
                    from_=TWILIO_NUMBER,
                    to="+8801773552776"
                )
        else:
            message = client.messages \
                .create(
                    body=f"{STOCK_NAME}: 🔻{round(diff_percentage)}%\nHeadline: {article["title"]}\n"
                         f"Brief: {article["description"]}",
                    from_=TWILIO_NUMBER,
                    to="+8801773552776"
                )
