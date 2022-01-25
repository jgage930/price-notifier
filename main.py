from bs4 import BeautifulSoup
import requests
import time
import smtplib
from config import email

def moneyToFloat(s:str) -> float:
    """giving a string in the form $1.00 convert to 1.00"""
    s = s[1:]
    return float(s)

def scrapePrice(url: str) -> float:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    current_price = soup.find(id="buy-box-product-price").text.strip()
    return moneyToFloat(current_price)

def sendEmail(price: float) -> None:
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    message = f"Cams are on sale for {str(price)}"
    s.sendmail(email, email, message)
    s.quit()

# Urls to scrape
rei_url = 'https://www.rei.com/product/138519/black-diamond-camalot-c4-cam'

base_low = 74.95 # base low price

while True:

    current_price = scrapePrice(rei_url)

    if current_price < base_low:
        sendEmail(current_price)
    
    time.sleep(60 * 60 * 3) # check every 3 hours