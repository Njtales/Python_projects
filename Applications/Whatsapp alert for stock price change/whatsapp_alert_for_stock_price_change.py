import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time
import pywhatkit
import pyautogui
from pynput.keyboard import Key, Controller

# Replace the placeholder with your Alpha Vantage API key
API_KEY = 'YOUR API KEY'

# Stock symbol for Microsoft
symbol = 'MSFT'

# Enter the percentage change you want to get alert for 
percent_alert = 0.0001

# Create a keyboard controller to send key presses
keyboard = Controller()

def send_whatsapp_message(msg: str):
    """
    Sends a WhatsApp message with the given message content.
    Assumes the user is already logged in to WhatsApp web.
    """
    try:
        pywhatkit.sendwhatmsg_instantly(
            phone_no="+{country code}{number}", 
            message=msg,
            tab_close=True
        )
        time.sleep(10)
        # Click the message send button
        pyautogui.click()
        time.sleep(2)
        # Send the message by pressing the enter key
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        print("Message sent!")
    except Exception as e:
        print(str(e))

# Get the intraday stock data for the given symbol
ts = TimeSeries(key=API_KEY, output_format='pandas')
data, meta_data = ts.get_intraday(symbol=symbol, interval='1min', outputsize='full')


# Get the close price data and calculate the percentage change
close_price = data['4. close']
percentage_change = close_price.pct_change()

# Get the percentage change of the latest available data point
latest_change = percentage_change[-1]

# If the percentage change exceeds the alert threshold, send a WhatsApp message
if abs(latest_change) > percent_alert :
    send_whatsapp_message(msg=f"{symbol} Alert : {latest_change}")
