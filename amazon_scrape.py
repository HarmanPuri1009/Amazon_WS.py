import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to extract data with error handling
def extract_data(tag, tag_type, class_name):
    element = tag.find(tag_type, {'class': class_name})
    if element:
        return element.text.strip()
    return ""

# Function to scrape Amazon product data
def scrape_amazon_products(url, pages):
    headers = {
        'User-Agent': 'Your User Agent String'  
    }

    product_data = {
        'Product URL': [],
        'Product Name': [],
        'Product Price': [],
        'Rating': [],
        'Number of Reviews': []
    }

    for page in range(1, pages + 1):
        page_url = f"{url}&page={page}"
        response = requests.get(page_url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.find_all('div', {'data-asin': True})

            for product in products:
                product_url_element = product.find('a', {'class': 'a-link-normal'})
                if product_url_element:
                    product_url = f"https://www.amazon.in{product_url_element['href']}"
                else:
                    product_url = "N/A"

                product_name = extract_data(product, 'span', 'a-text-normal')
                product_price = extract_data(product, 'span', 'a-price-whole')
                rating = extract_data(product, 'span', 'a-icon-alt')
                num_reviews = extract_data(product, 'span', 'a-size-base')

                product_data['Product URL'].append(product_url)
                product_data['Product Name'].append(product_name)
                product_data['Product Price'].append(product_price)
                product_data['Rating'].append(rating)
                product_data['Number of Reviews'].append(num_reviews)

            print(f"Scraped page {page}")
        else:
            print(f"Failed to fetch data from page {page}")

    return pd.DataFrame(product_data)
amazon_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
pages_to_scrape = 20
amazon_data = scrape_amazon_products(amazon_url, pages_to_scrape)
amazon_data.to_csv('amazon_products_20_pages.csv', index=False)
