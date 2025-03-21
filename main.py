
from bs4 import BeautifulSoup
import requests
import smtplib
import os
from dotenv import load_dotenv

# load env variables
load_dotenv(override = True)

smtp_address = os.getenv("SMTP_ADDRESS")
email_address = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")

url = "https://www.amazon.com/dp/B0B2GF9GKL?tag=mywishli-20&linkCode=osi&th=1&psc=1"
header = {
     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
     "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get(url, headers=header)

soup = BeautifulSoup(response.content, "html.parser")
# check if we get the actual Amazon page
print(soup.prettify())
# Find the HTML element that contains the price
price = soup.find(class_="a-offscreen").get_text()
# Remove the dollar sign using split
price_without_currency = price.split("$")[1]
# Convert to floating point number
price_as_float = float(price_without_currency)
print(price_as_float)

# send an email notification
# get the product title

title = soup.find(id = "productTitle").get_text().strip()
print(title)

# set the price threshold

PRICE = 13

if price_as_float < PRICE:
    message = f"{title} is on sale for {price}!"

    with smtplib.SMTP(smtp_address, 587) as connection:
        connection.starttls()
        result = connection.login(email_address, email_password)
        connection.sendmail(
            from_addr=email_address,
            to_addrs=email_address,
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}".encode("utf-8")
        )


