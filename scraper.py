import time
import asyncio
import logging
from decimal import Decimal
from uuid import uuid4
from pathlib import Path

import aiofiles
import httpx
from bs4 import BeautifulSoup
from price_parser import Price
from pydantic import BaseModel


BASE_URL = 'https://shop.poohcorner.co.uk/'
OUTPUT_DIR = Path('output')
IMAGE_OUTPUT_DIR = OUTPUT_DIR / 'images'

limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
client = httpx.AsyncClient(timeout=10.0, limits=limits)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

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


async def fetch_page(url: str) -> BeautifulSoup:
    response = await client.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'lxml')


async def save_photo_async(url: str) -> str:
    response = await client.get(f'https:{url}')

    if response.status_code != 200:
        raise ValueError(f"Wrong status code {response.status_code} while requesting image")

    filename = f'{IMAGE_OUTPUT_DIR}/{uuid4()}.png'

    async with aiofiles.open(filename, 'wb') as image_file:
        await image_file.write(response.content)

    return filename


async def extract_product(sub_url: str) -> Product:
    page = await fetch_page(f'{BASE_URL}{sub_url}')

    product_name = page.find('h1').text
    product_description_container = page.find('div', class_='product-short-description rte')
    product_price_str = page.find('span', class_='amount').text
    product_image_url = page.find('product-slider').div.a['href']

    product_description = product_description_container.get_text()
    product_price = Price.fromstring(product_price_str)

    image_src = await save_photo_async(product_image_url)

    product = Product(
        name=product_name,
        description=product_description,
        price=product_price.amount,
        currency=product_price.currency,
        images=[image_src]
    )

    logging.info(f"Extracted product: {product_name}")

    return product


async def extract_subcategory(sub_url: str) -> Subcategory:
    page = await fetch_page(f'{BASE_URL}{sub_url}')

    subcategory_name = page.find('h1').text
    products = page.find_all('product-card')
    products_urls: list[str] = [p.figure.a['href'] for p in products]

    products_list = await asyncio.gather(*(extract_product(url) for url in products_urls))

    subcategory = Subcategory(
        name=subcategory_name,
        products=products_list
    )

    logging.info(f"Successfully extracted all products from subcategory {subcategory_name}")

    return subcategory


async def extract_categories() -> list[Category]:
    page = await fetch_page(BASE_URL)

    html_categories = page.find_all('li', class_='menu-item-has-children')
    categories: list[Category] = []

    for html_category in html_categories:
        category_name = html_category.a.text.strip()
        html_subcategories = html_category.ul.find_all('a')
        subcategories_urls: list[str] = [s['href'] for s in html_subcategories]

        subcategories_list = await asyncio.gather(*(extract_subcategory(url) for url in subcategories_urls))

        category = Category(
            name=category_name,
            subcategories=subcategories_list
        )

        logging.info(f"Successfully extracted category: {category_name}")

        categories.append(category)

    return categories


async def main():
    start_time = time.perf_counter()

    OUTPUT_DIR.mkdir(exist_ok=True)
    IMAGE_OUTPUT_DIR.mkdir(exist_ok=True)

    categories = Categories(
        categories=await extract_categories()
    )

    filename = f'{OUTPUT_DIR}/output.json'
    with open(filename, 'w', encoding='utf-8') as json_file:
        json_file.write(categories.model_dump_json())

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time:.5f} seconds")


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) # Set event loop policy (Windows only)
    asyncio.run(main())
