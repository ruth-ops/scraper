import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://books.toscrape.com/"
# Attempt to connect to website if the connection fails
try:
        response = requests.get(url)
        response.encoding = "utf-8"
except:
        print("could not connect to the website")
        exit()

#  exchange rate from the web api
api_url = "https://v6.exchangerate-api.com/v6/bb77ba4d737ab5559c695f49/latest/GBP"
api_response = requests.get(api_url)
api_data = api_response.json()
rate = api_data["conversion_rates"]["KES"]

soup = BeautifulSoup(response.text, 'html.parser')
# find all the books
books = soup.find_all("article", class_="product_pod")
print(response.status_code)
book_list = [] # creating an empty list to store the book data

# loop through the first 10 books and print their title and price
for book in books[:10]:
    title = book.select_one("h3 a")["title"]
    price_text = book.select_one(".price_color").text
    # convert the price  from £ to kes

    original_price = float(price_text.replace("£", ""))
    final_price = round(original_price * rate, 2)
    print(title, "final price:", final_price)
    book_list.append({"title": title,
                      "original_price": original_price,
                      "final_price": final_price
                      })
    # pandas dataframe to store the book data
    df = pd.DataFrame(book_list)
    # display the dataframe
    print("\nBook price(GBP to KES):")
    print(df.to_string(index=False))
    # saving the data to a csv file
    df.to_csv("book_prices.csv", index=False)
    print("Data saved to book_prices.csv")