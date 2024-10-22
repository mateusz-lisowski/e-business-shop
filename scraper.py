from pydantic import BaseModel


BASE_URL = 'https://shop.poohcorner.co.uk/'


class Product(BaseModel):
    name: str
    description: str
    price: float
    currency: str
    images: list[str]


class Subcategory(BaseModel):
    name: str
    products: list[Product]


class Category(BaseModel):
    name: str
    subcategories: list[Subcategory]


def extract_categories():
    pass


def extract_product():
    pass


def main():
    pass


if __name__ == '__main__':
    main()
