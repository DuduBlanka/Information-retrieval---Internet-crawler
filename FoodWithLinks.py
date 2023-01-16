import requests
import csv
from bs4 import BeautifulSoup
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googletrans import Translator
from selenium import webdriver




def getWeight(str, name, weight_List):
    # Create a new webdriver object
    grab_from_span = False
    weight_and_unit = None

    # Navigate to the product page
    driver.get(str)

    # Retrieve the HTML of the product page
    product_html = driver.page_source
    product_soup = BeautifulSoup(product_html, 'html.parser')

    labels = product_soup.find_all('label', class_=['d-block option', 'd-block option active'])
    for label in labels:
        weight = label.find('b').text
        if 'ק"ג' in weight or 'מ"ל' in weight:
            weight_and_unit = f"{weight}"
            if (name,weight_and_unit,product_link) not in weight_List:
                weight_List.append((name,weight_and_unit,product_link))
        else:
            grab_from_span = True
            break
    if weight_and_unit is None or grab_from_span == True:
     
     span_elements = product_soup.find_all('span', class_='prWeight')

     for span in span_elements:
        weight = span.text
        if span.next_sibling:
            if span.next_sibling.string:
                weight_units = span.next_sibling.string.strip()
                if weight_units == 'מ"ל' or weight_units == 'ק"ג' or weight_units == 'גרם':
                    weight_and_unit = weight + ' ' + weight_units
                    if (name,weight_and_unit,product_link) not in weight_List:
                     weight_List.append((name,weight_and_unit,product_link))

                else:
                # Set the weight unit to an empty string
                 unit = ''
        else:
            # Set the weight unit to an empty string
            unit = ''

   
#product_Weight2 = product_soup.find('div',class_='data-weight')
#product_name = product_soup.find('h1').text
#product_weight = product_soup.find('span', class_='prWeight').text

# Store the product name and weight in the dictionary
#products[product_name] = product_weight

# Close the webdriver
# print(products)

#driver.close()





















session = requests.Session()
driver = webdriver.Chrome()

# Initialize the page number and results list
page = 1

# Set the maximum number of pages to retrieve
max_pages = 4

weight_results = []

while page <= max_pages:
    # Send a POST request to the search form with the desired query and page number
    url = 'https://www.anipet.co.il/Cat/0/?keyword=%D7%9E%D7%96%D7%95%D7%9F'
    data = {'q': 'מזון', 'page': page}
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
        getWeight(product_link,product_name,weight_results)
        # Follow the link and retrieve the product page
    # Add the translated results to the overall results list
#    results.extend(translated_results)

    # Increment the page number
    page += 1


encode_list = [tuple(s.encode('utf-8-sig') for s in t) for t in weight_results]


# Open the CSV file for writing
with open('FoodProductsWeight.csv', 'w', encoding='utf-8-sig', newline='') as csv_file:
    # Create a CSV writer object
    csv_writer = csv.writer(csv_file)

    # Write the header row
    csv_writer.writerow(['Product Name', 'Product Weight','Product Link'])

    # Write the tuples to the CSV file
    for product_name, product_category,product_link in encode_list:
        decoded_name = product_name.decode('utf-8-sig')
        decoded_category = product_category.decode('utf-8-sig')
        decoded_product_link = product_link.decode('utf-8-sig')
        csv_writer.writerow([decoded_name, decoded_category,decoded_product_link])

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
  #          f.write(result + '\n')