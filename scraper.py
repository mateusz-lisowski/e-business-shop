import time
from decimal import Decimal
from uuid import uuid4
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from price_parser import Price
from pydantic import BaseModel


BASE_URL = 'https://shop.poohcorner.co.uk/'
OUTPUT_DIR = Path('output')
IMAGE_OUTPUT_DIR = OUTPUT_DIR / 'images'


class Product(BaseModel):
    name: str
    description: str
    price: Decimal
    currency: str
    images: list[str]


class Subcategory(BaseModel):
    name: str
    products: list[Product]


class Category(BaseModel):
    name: str
    subcategories: list[Subcategory]


class Categories(BaseModel):
    categories: list[Category]


def save_photo(url: str) -> str:
    response = requests.get(f'https:{url}')

    if response.status_code != 200:
        raise ValueError(f"Wrong status code {response.status_code} while requesting image")

    filename = f'{IMAGE_OUTPUT_DIR}/{uuid4()}.png'
    with open(filename, 'wb') as image_file:
        image_file.write(response.content)

    return filename


def extract_product(sub_url: str) -> Product:
    response = requests.get(f'{BASE_URL}{sub_url}')
    if response.status_code != 200:
        raise ValueError(f"Wrong status code {response.status_code} while requesting product page")

    page = BeautifulSoup(response.text, 'lxml')

    product_name = page.find('h1').text
    product_description_container = page.find('div', class_='product-short-description rte')
    product_price_str = page.find('span', class_='amount').text
    product_image_url = page.find('product-slider').div.a['href']

    product_description = product_description_container.get_text()
    product_price = Price.fromstring(product_price_str)
    image_src = save_photo(product_image_url)

    product = Product(
        name=product_name,
        description=product_description,
        price=product_price.amount,
        currency=product_price.currency,
        images=[image_src]
    )

    print(f"Extracted product: {product}")

    return product


def extract_subcategory(sub_url: str) -> Subcategory:
    response = requests.get(f'{BASE_URL}{sub_url}')
    if response.status_code != 200:
        raise ValueError(f"Wrong status code {response.status_code} while requesting subcategory page")

    page = BeautifulSoup(response.text, 'lxml')

    subcategory_name = page.find('h1').text
    products = page.find_all('product-card')
    products_urls: list[str] = [p.figure.a['href'] for p in products]

    subcategory = Subcategory(
        name=subcategory_name,
        products=[extract_product(url) for url in products_urls]
    )

    print(f"Successfully extracted all products from subcategory {subcategory_name}")

    return subcategory


def extract_categories() -> list[Category]:
    categories: list[Category] = []

    response = requests.get(BASE_URL)
    if response.status_code != 200:
        raise ValueError(f"Wrong status code {response.status_code} while requesting main page")

    page = BeautifulSoup(response.text, 'lxml')

    html_categories = page.find_all('li', class_='menu-item-has-children')

    for html_category in html_categories:
        category_name = html_category.a.text.strip()
        html_subcategories = html_category.ul.find_all('a')
        subcategories_urls: list[str] = [s['href'] for s in html_subcategories]
        category = Category(
            name=category_name,
            subcategories=[extract_subcategory(url) for url in subcategories_urls]
        )
        print(f"Successfully extracted all subcategories from category {category_name}")
        categories.append(category)

    return categories


def main():
    start_time = time.time()

    OUTPUT_DIR.mkdir(exist_ok=True)
    IMAGE_OUTPUT_DIR.mkdir(exist_ok=True)

    categories = Categories(
        categories=extract_categories()
    )

    print(categories)

    filename = f'{OUTPUT_DIR}/output.json'
    with open(filename, 'w', encoding='utf-8') as json_file:
        json_file.write(categories.model_dump_json())

    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time:.5f} seconds")

if __name__ == '__main__':
    main()
