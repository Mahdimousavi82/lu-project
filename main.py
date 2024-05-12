import csv
import requests
import matplotlib.pyplot as plt
import pandas as pd

# تابع برای دانلود داده ها و ذخیره آن در فایل CSV
def fetch_currency_data(url, filename, currency_pair, step, limit):
    """
    این تابع داده ها را از API با توجه به پارامترهای ارائه شده دانلود کرده و در یک فایل CSV ذخیره می کند.

    Args:
        url (str): URL API
        filename (str): نام فایل CSV برای ذخیره داده ها
        currency_pair (str): جفت ارز مورد نظر (مانند BTC-USD)
        step (str): بازه زمانی (مانند 1h، 1d، 1w)
        limit (int): تعداد نقاط داده برای دانلود
    """
    try:
        response = requests.get(url.format(currency_pair=currency_pair, step=step, limit=limit))
        data = response.json()

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["timestamp", "price"])

            for row in data:
                timestamp = int(row["timestamp"])  # تبدیل timestamp به عدد صحیح
                price = float(row["price"])
                writer.writerow([timestamp, price])

    except Exception as e:
        print(f"Error: {e}")

# تابع برای بارگذاری قیمت ها از فایل CSV
def load_price_data(filename):
    """
    این تابع قیمت ها را از یک فایل CSV بارگیری می کند و به عنوان یک دیکشنری برمی گرداند.

    Args:
        filename (str): نام فایل CSV

    Returns:
        dict: دیکشنری قیمت ها با کلید timestamp و مقادیر قیمت
    """
    try:
        data = pd.read_csv(filename)
        prices = dict(zip(data['timestamp'], data['price']))
        return prices
    except Exception as e:
        print(f"Error: {e}")
        return {}

# تابع برای ذخیره قیمت ها در یک فایل JSON
def save_prices_to_json(prices, filename):
    """
    این تابع قیمت ها را در یک فایل JSON ذخیره می کند.

    Args:
        prices (dict): دیکشنری قیمت ها با کلید timestamp و مقادیر قیمت
        filename (str): نام فایل JSON
    """
    try:
        with open(filename, 'w') as jsonfile:
            json.dump(prices, jsonfile)
    except Exception as e:
        print(f"Error: {e}")

# تابع برای محاسبه میانگین قیمت ها
def calculate_mean_price(prices):
    """
    این تابع میانگین قیمت ها را از یک دیکشنری قیمت ها محاسبه می کند.

    Args:
        prices (dict): دیکشنری قیمت ها با کلید timestamp و مقادیر قیمت

    Returns:
        float: میانگین قیمت ها
    """
    if not prices:
        return 0
    return mean(prices.values())  # از تابع mean کتابخانه آمار پایتون استفاده کنید

# تابع برای رسم میانگین قیمت
def plot_mean_price(prices, average_price):
    """
    این تابع میانگین قیمت را روی نمودار قیمت ها رسم می کند.

    Args:
        prices (dict): دیکشنری قیمت ها با کلید timestamp و مقادیر قیمت
        average_price (float): میانگین قیمت
    """
    plt.plot(prices.keys(), prices.values(), label='قیمت')
    plt.axhline(y=average_price, color='red', label='میانگین قیمت')
    plt.xlabel('زمان')
    plt.ylabel('قیمت')
    plt.title('قیمت در طول زمان با میانگین قیمت')
    plt.legend()
    plt.show()

# مثال استفاده

# پارامترها را تنظیم کنید
currency_pair = "btcusd"  # جفت ارز مورد نظر
step = "3600"  # بازه زمانی
limit = 100  # تعداد نقاط داده

# دانلود داده ها
url = f"https://www.bitstamp.net/api/v2/ohlc/{currency_pair}/?step={step}&limit={limit}"

print(url)
fetch_currency_data(url, "data.csv", currency_pair, step, limit)

# بارگذاری قیمت ها
prices = load_price_data("data.csv")

# محاسبه میانگین قیمت
