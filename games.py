import requests
import csv
from bs4 import BeautifulSoup
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googletrans import Translator
from selenium import webdriver





def getGame(str):
# Create a new webdriver object
 products = {}

# Navigate to the product page
 driver.get(str)

# Retrieve the HTML of the product page
 product_html = driver.page_source

 product_soup = BeautifulSoup(product_html, 'html.parser')
 game_description = product_soup.find_all('div',class_='description')
 category = 'אין קטגוריה'
# Print the text of each element
 for games in game_description:
        # Extract the text of the element
    search_result = games.text
    # Check if the text contains the word "אסטרטגיה"
    if "אסטרטגיה" in search_result:
        # Save the text
        category = 'אסטרטגיה'
    elif "עיסוי" in search_result:
        category = 'עיסוי'
    elif "גירוי" in search_result:
        category = 'גירוי'
 return category
#product_Weight2 = product_soup.find('div',class_='data-weight')
#product_name = product_soup.find('h1').text
#product_weight = product_soup.find('span', class_='prWeight').text

# Store the product name and weight in the dictionary
#products[product_name] = product_weight

# Close the webdriver
# print(products)






















session = requests.Session()
driver = webdriver.Chrome()

# Initialize the page number and results list
page = 1

# Set the maximum number of pages to retrieve
max_pages = 1

games_list = []

while page <= max_pages:
    # Send a POST request to the search form with the desired query and page number
    url = 'https://www.anipet.co.il/Cat/0/?keyword=%D7%9E%D7%A9%D7%97%D7%A7+%D7%9C%D7%9B%D7%9C%D7%91'
    data = {'q': 'משחק לכלב', 'page': page}
    response = session.post(url, data=data)

    # Retrieve the search results page
    html = response.text

    # Parse the HTML and extract the search results
    soup = BeautifulSoup(html, 'html.parser')
    page_results = soup.find_all('div', class_='details')

    # Translate the page results from Hebrew to English
    for result in page_results:
        text = result.text
        product_name = result.find('h5',class_='title').text
        product_link = result.find('a')['href']
        product_link = 'https://www.anipet.co.il' + product_link
        product_gameCategory = getGame(product_link)
        games_list.append((product_name,product_gameCategory))
        # Follow the link and retrieve the product page


    # Increment the page number
    page += 1



encode_list = [tuple(s.encode('utf-8-sig') for s in t) for t in games_list]


# Open the CSV file for writing
with open('Games.csv', 'w', encoding='utf-8-sig', newline='') as csv_file:
    # Create a CSV writer object
    csv_writer = csv.writer(csv_file)

    # Write the header row
    csv_writer.writerow(['Product Name', 'Game Category'])

    # Write the tuples to the CSV file
    for product_name, product_category in encode_list:
        decoded_name = product_name.decode('utf-8-sig')
        decoded_category = product_category.decode('utf-8-sig')
        csv_writer.writerow([decoded_name, decoded_category])

driver.close()
































#url = 'https://www.anipet.co.il/Cat/0/?keyword=%D7%9E%D7%96%D7%95%D7%9F'
#response = requests.get(url)
#html = response.text


#soup = BeautifulSoup(html, 'html.parser')
#results = soup.find_all('div', class_='details')

#translated_text = translator.translate(results, dest='en')

#translated_results = []
#for result in results:
 #   text = result.text
  #  translated_text = translator.translate(text, dest='en').text
  #  translated_results.append(translated_text)

#with open('translated_results.txt', 'w', encoding="utf-8") as f:
 #       for result in translated_results:
  #          f.write(result + '\n')