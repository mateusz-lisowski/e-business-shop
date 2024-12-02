import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


ROOT_URL = 'http://localhost:8080/pl/'


def test_add_products_to_cart(driver: WebDriver):

    # Fetch all categories
    categories_links = driver.find_elements(By.CLASS_NAME, 'dropdown-item')

    # Choose random categories
    categories_links = random.sample(categories_links, 2)

    # Extract categories links
    categories_links = [c.get_attribute('href') for c in categories_links]

    for category_link in categories_links:

        # Navigate to category page
        driver.get(category_link)

        # Fetch all products on page
        products_links = driver.find_elements(By.CSS_SELECTOR, '.thumbnail.product-thumbnail')

        # Choose random products
        try:
            products_links = random.sample(products_links, 5)
        except ValueError:
            print(f"Number of products less than wanted: {len(products_links)}")

        # Extract categories links
        products_links = [p.get_attribute('href') for p in products_links]

        for product_link in products_links:

            # Navigate to product page
            driver.get(product_link)

            # Get quantity button
            quantity_button = driver.find_element(
                By.CSS_SELECTOR,
                '.btn.btn-touchspin.js-touchspin.bootstrap-touchspin-up'
            )

            # Increase products quantity
            for _ in range(random.randrange(10)):
                quantity_button.click()

            # Get purchase button
            button = driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary.add-to-cart')

            # Purchase product
            button.click()


def test_search_by_product_name_and_add_random_to_cart(driver: WebDriver, wait: WebDriverWait):

    # Get search input element
    search_input = driver.find_element(By.CLASS_NAME, 'ui-autocomplete-input')

    # Enter searched phrase to input
    search_input.send_keys('pooh\n')

    # Fetch all products on page
    products_links = wait.until(
        ec.visibility_of_all_elements_located((By.CSS_SELECTOR, '.thumbnail.product-thumbnail'))
    )

    # Choose random product
    product_link = random.choice(products_links)

    # Navigate to product page
    driver.get(product_link.get_attribute('href'))

    # Get purchase button
    button = driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary.add-to-cart')

    # Purchase product
    button.click()


def test_remove_products_from_cart(driver: WebDriver):

    # Navigate to cart page
    driver.get('http://localhost:8080/pl/cart?action=show')

    # Fetch all delete links
    delete_links = driver.find_elements(By.CLASS_NAME, 'remove-from-cart')

    # Choose few links to delete
    delete_links = random.sample(delete_links, 3)

    # Extract categories links
    delete_links = [d.get_attribute('href') for d in delete_links]

    for delete_link in delete_links:
        driver.get(delete_link)


def test_register_new_account(driver):
    pass


def test_order_cart_contents(driver):
    pass


def test_order_with_payment_method(driver):
    pass


def test_chose_one_carrier(driver):
    pass


def test_accept_order(driver):
    pass


def test_check_order_status(driver):
    pass


def test_download_vat_invoice(driver):
    pass


def main():

    # Setup
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    driver.get(ROOT_URL)

    # Tests
    # test_add_products_to_cart(driver)
    # test_search_by_product_name_and_add_random_to_cart(driver, wait)
    # test_remove_products_from_cart(driver)

    # Close driver
    driver.quit()


if __name__ == '__main__':
    main()
