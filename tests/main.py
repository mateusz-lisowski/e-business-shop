import random
import time
import uuid

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


ROOT_URL = 'http://localhost:8080/pl/'


def test_add_products_to_cart(driver: WebDriver):

    # Navigate to main page
    driver.get(ROOT_URL)

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

            # Wait for product to purchase
            time.sleep(1)


def test_search_by_product_name_and_add_random_to_cart(driver: WebDriver, wait: WebDriverWait):

    # Navigate to main page
    driver.get(ROOT_URL)

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

    # Wait for product to purchase
    time.sleep(1)


def test_remove_products_from_cart(driver: WebDriver):

    # Navigate to cart page
    driver.get('http://localhost:8080/pl/cart?action=show')

    # Fetch all delete links
    delete_links = driver.find_elements(By.CLASS_NAME, 'remove-from-cart')

    # Choose few links to delete
    try:
        delete_links = random.sample(delete_links, 3)
    except ValueError:
        print(f"Number of products less than wanted: {len(delete_links)}")

    for delete_link in delete_links:

        # Delete product
        delete_link.click()


def test_register_new_account(driver: WebDriver):

    # Navigate to register account page
    driver.get('http://localhost:8080/pl/login?create_account=1')

    # Get first name input element
    firstname_input = driver.find_element(By.ID, 'field-firstname')

    # Input first name
    firstname_input.send_keys('Matt')

    # Get last name input element
    lastname_input = driver.find_element(By.ID, 'field-lastname')

    # Input last name
    lastname_input.send_keys('Damon')

    # Get email input element
    email_input = driver.find_element(By.ID, 'field-email')

    # Input email
    email_input.send_keys(f'matt.damon.{uuid.uuid4()}@email.com')

    # Get password input element
    password_input = driver.find_element(By.ID, 'field-password')

    # Input password
    password_input.send_keys('admin')

    # Get privacy info checkbox
    privacy_info_checkbox = driver.find_element(By.NAME, 'customer_privacy')

    # Check privacy info checkbox
    privacy_info_checkbox.click()

    # Get accept privacy policy checkbox
    privacy_policy_checkbox = driver.find_element(By.NAME, 'psgdpr')

    # Check privacy policy checkbox
    privacy_policy_checkbox.click()

    # Get save customer button
    save_customer_button = driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary.form-control-submit.float-xs-right')

    # Save customer
    save_customer_button.click()

    # Wait for customer to be saved
    time.sleep(1)


def test_order_cart_content(driver: WebDriver):

    # Navigate to cart page
    driver.get('http://localhost:8080/pl/cart?action=show')

    # Get purchase button
    purchase_button = driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary')

    # Press purchase button
    purchase_button.click()

    # Get address input element
    address_input = driver.find_element(By.ID, 'field-address1')

    # Input address
    address_input.send_keys('Downing Street')

    # Get postal code input element
    postal_code_input = driver.find_element(By.ID, 'field-postcode')

    # Input postal code
    postal_code_input.send_keys('70-010')

    # Get city input element
    city_input = driver.find_element(By.ID, 'field-city')

    # Input city
    city_input.send_keys('London')

    # Get next button
    next_address_button = driver.find_element(By.NAME, 'confirm-addresses')

    # Navigate to next section
    next_address_button.click()

    # Get delivery checkbox
    delivery_checkbox = driver.find_element(By.ID, 'delivery_option_3')

    # Check delivery checkbox
    delivery_checkbox.click()

    # Get next button
    next_delivery_button = driver.find_element(By.NAME, 'confirmDeliveryOption')

    # Navigate to next section
    next_delivery_button.click()

    # Get payment option button
    payment_option = driver.find_element(By.ID, 'payment-option-3')

    # Chose given payment method
    payment_option.click()

    # Get approve conditions checkbox
    approve_conditions_button = driver.find_element(By.ID, 'conditions_to_approve[terms-and-conditions]')

    # Check approve conditions checkbox
    approve_conditions_button.click()

    # Get indent button
    indent_button = driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary.center-block')

    # Place an order
    indent_button.click()

    # Wait for order to be processed
    time.sleep(1)


def test_check_order_status(driver: WebDriver):

    # Navigate to order history page
    driver.get('http://localhost:8080/pl/order-history')

    # Get all links on page
    links = driver.find_elements(By.TAG_NAME, 'a')

    # Find link order detail link
    details_link: str | None = None
    for link in links:
        if 'controller=order-detail' in link.get_attribute('href'):
            details_link = link.get_attribute('href')
            break

    # Navigate to order details page
    driver.get(details_link)


def test_download_vat_invoice(driver):
    pass


def main():

    # Setup
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    start_time = time.perf_counter()

    # Tests
    test_add_products_to_cart(driver)
    test_search_by_product_name_and_add_random_to_cart(driver, wait)
    test_remove_products_from_cart(driver)
    test_register_new_account(driver)
    test_order_cart_content(driver)
    test_check_order_status(driver)

    end_time = time.perf_counter()

    # Close driver
    driver.quit()

    # Calculate time taken by tests
    print(f"Tests took: {(end_time - start_time):.2f}s")

if __name__ == '__main__':
    main()
