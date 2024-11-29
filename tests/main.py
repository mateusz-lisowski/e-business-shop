from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


ROOT_URL = 'http://localhost:8080/gb/'


def test_add_products_to_cart(driver):
    category1 = driver.get_element(By.CLASS_NAME, "information")


def test_search_by_product_name_and_add_random_to_cart(driver):
    pass


def test_remove_products_from_cart(driver):
    pass


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
    driver = webdriver.Chrome()
    driver.quit()


if __name__ == '__main__':
    main()
