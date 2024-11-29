import time

from selenium import webdriver


ROOT_URL = 'http://localhost:8080/gb/'


def main():
    driver = webdriver.Chrome()
    driver.get(ROOT_URL)
    time.sleep(10)
    driver.quit()


if __name__ == '__main__':
    main()
