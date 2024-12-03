from prestapyt import PrestaShopWebServiceDict, PrestaShopWebServiceError  
import re
import json
import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
import os
import base64
from dotenv import load_dotenv

load_dotenv()
API_URL = 'http://localhost:8080/api'
API_KEY = os.getenv("API_KEY")

# connecting to API
prestashop = PrestaShopWebServiceDict(API_URL, API_KEY)


'''
function for adding new category to prestashop,
prestashop - API connection object 
parent_ID - ID Of parent category, default id = 2 is for category HOME

return - (int) id of added category or None if error occured
'''
def add_category(prestashop: PrestaShopWebServiceDict, category_name: str, parent_id=2) -> int:
    category_data = {
        'category': {
            'id_parent': parent_id,
            'active': '1',
            'name': {'language': [{'attrs': {'id': '1'}, 'value': category_name}]},
            'link_rewrite': {'language': [{'attrs': {'id': '1'}, 'value': generate_link_rewrite(category_name)}]}
        }
    }
    try:
        result = prestashop.add('categories', category_data)
        category_id = result['prestashop']['category']['id']
        print(f"Success: added '{category_name}' with ID {category_id}")
        return category_id
    except PrestaShopWebServiceError as e:
        print(f"error occured during add category '{category_name}': {e}")
        return None
    
def generate_link_rewrite(name):
    return re.sub(r'\W+', '-', name.lower()).strip('-')


'''
function for adding product to prestashop
arguments:
prestashop - (PrestaShopWebServiceDict) prestashop connection object
product_name - (str) name of product
product_description - (str) product description
product_short_description - (str) short version of description
product_price - (float) price
main_category_id - (string) id of main category 
categories_id - (string) id of additional categories related to product

return - (int) id of added product, or None if error occured
'''
def add_product(prestashop: PrestaShopWebServiceDict, product_name: str, product_description: str, product_short_description: str, product_price: float, main_category_id: str, categories_ids: list[str]) -> int:
    product_data = {
        'product': {
            'active': '1',  
            'state':'1', #required for products to show in catalog/products
            'redirect_type': '301-category',
            'visibility': 'both',
            'name': {'language': [{'attrs': {'id': '1'}, 'value': product_name}]},  
            'price': str(product_price),  
            'id_category_default': main_category_id,  
            'id_default_category': main_category_id,
            'id_tax_rules_group': '1',  
            'description': {'language': [{'attrs': {'id': '1'}, 'value': product_description}]},  
            'description_short': {'language': [{'attrs': {'id': '1'}, 'value': product_short_description}]},  
            'link_rewrite': {'language': [{'attrs': {'id': '1'}, 'value': generate_link_rewrite(product_name)}]}, 
            'associations': {
                #'categories': [{'id': main_category_id}] + [{'id': category_id} for category_id in categories_ids]
                'categories': {
                    'category': [
                        {'id': main_category_id},
                        #secondary categories
                    ]
                }
            }
        }
    }

    try:
        result = prestashop.add('products', product_data)
        print(f"Success: added'{product_name}' with ID {result['prestashop']['product']['id']}")
        return result['prestashop']['product']['id']
    except PrestaShopWebServiceError as e:
        print(f"error during add product '{product_name}': {e}")
        return None



"""
function adds all categories and products from given json file to shop

arguments:
filepath (str): path to the json file which contains result of web scrapping

return (list[str], dict{id:image_path}): list with ids of new added products, dict with ids and related images
"""
def addProducts(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as plik:
        products_data = json.load(plik)

    category_ids = {} # dictionary for storing ids of categories added to shop {name: id}
    product_with_categories = {}  # dictionary for storing products with informations about them {product_name:{'price':price, 'description':desc,'categories':[categories_ids]}}
    products_ids = []
    images = {} # dictionary in form - {product_id: image_path}
    for category in products_data['categories']:
        main_category_name = category['name']

        if main_category_name not in category_ids:
            category_ids[main_category_name] = add_category(prestashop, main_category_name)

        for subcategory in category['subcategories']:
            subcategory_name = subcategory['name']

            if subcategory_name not in category_ids:
                category_ids[subcategory_name] = add_category(prestashop, subcategory_name, parent_id=category_ids[main_category_name])

            for product in subcategory['products']:
                if product['name'] not in product_with_categories:
                    # retrieving id of product
                    product_with_categories[product['name']] = {'description':product['description'],'price':product['price'],'currency':product['currency'],'images':product['images'] ,'categories':[category_ids[subcategory_name]]}
                else:
                    product_with_categories[product['name']]['categories'].append(category_ids[subcategory_name])

    for product, data in product_with_categories.items():
        product_id = add_product(prestashop, product, data['description'], data['description'][:100], (data['price'].replace(',', '.')), data['categories'][0], data['categories'][1:] if len(data['categories'])>0 else [])
        if product_id is not None:
            products_ids.append(product_id)
            images[product_id] = data['images']
    
    return products_ids, images


'''
function addStocks sends information about current stocks of given products to prestashop
arguments:
ids: list with ids of products we want to change stocks

'''
def addStocks(ids: list[str]):
    for product_id in ids:
        api_url = API_URL + "/stock_availables"

        quantity_to_add = 420

        response = requests.get(f"{api_url}?filter[id_product]={product_id}", auth=HTTPBasicAuth(API_KEY, ''))

        if response.status_code == 200:
            stock_available = ET.fromstring(response.content)
            stock_id = stock_available.find('.//stock_available').attrib['id']
        else:
            print("Error while fetching stock availability:", response.content)
            exit()

        update_data = f'''<?xml version="1.0" encoding="UTF-8"?>
        <prestashop>
            <stock_available>
                <id>{stock_id}</id> 
                <id_product>{product_id}</id_product>
                <id_product_attribute>0</id_product_attribute>
                <quantity>{quantity_to_add}</quantity> 
                <depends_on_stock>0</depends_on_stock>
                <out_of_stock>0</out_of_stock>
                <id_shop>1</id_shop>
            </stock_available>
        </prestashop>'''


        update_response = requests.put(f"{api_url}/{stock_id}", data=update_data, headers={"Content-Type": "application/xml"}, auth=HTTPBasicAuth(API_KEY, ''))
        if update_response.status_code == 200:
            print("Quantity successfully updated for id: ", product_id )
        else:
            print("Error while updating availability:", update_response.content)


'''
function for uploading images to prestashop
arguments:
product_id (str): id of product, which image will be updated
image_path (str): relative path to image

'''
def upload_product_image(product_id: str, image_path: str):
        if not os.path.isfile(image_path):
            print(f"Plik {image_path} nie istnieje.")
            return

        headers = {
            'Authorization': f'Basic {base64.b64encode(f"{API_KEY}:".encode()).decode()}',
        }

        api_URL = f"{API_URL}/images/products/{product_id}"

        with open(image_path, 'rb') as image_file:
            files = {
                'image': (os.path.basename(image_path), image_file, 'image/jpeg')  
            }

            try:
                response = requests.post(api_URL, headers=headers, files=files)

                if response.status_code in [200, 201]: 
                    print("image uploaded successfully!")
                else:
                    print(f"Error during uploading image: {response.content.decode()}")

            except requests.exceptions.RequestException as e:
                print(f"Error during uploading image: {e}")


'''
uploading images of all products
args:
images_info (dict{id:[image_paths]}): info of images related to product with given id
'''
current_dir = os.path.dirname(__file__)
def upload_all_images(images_info):
    for id, images in images_info.items():
        for image in images:
            upload_product_image(id, str(current_dir)+'\\images\\'+str(image))


def main():
    ids, image_info = addProducts(str(os.path.dirname(__file__))+"\\output.json")

    addStocks(ids)
    upload_all_images(image_info)

if __name__ == "__main__":
    main()


