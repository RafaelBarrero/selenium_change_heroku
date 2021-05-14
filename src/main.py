import sys
import time

from config.settings import *

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


def main():

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome('chromedriver', options=chrome_options)
    driver.delete_all_cookies()

    i = 0
    while i < 2:
        if len(sys.argv) > 1 and sys.argv[1].lower() == "alter":
            if i == 0:
                email = ALTER
            else:
                email = MAIN
        else:
            if i == 0:
                email = MAIN
            else:
                email = ALTER

        driver.get("https://id.heroku.com/login")

        # Email
        WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.ID, 'email'))).send_keys(email)

        # Password
        driver.find_element_by_id("password").send_keys(PASSWORD)

        # Log in
        driver.find_element_by_name("commit").click()

        # No 2Factor. Not always
        try:
            WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.CLASS_NAME, 'btn-link'))).click()
        except TimeoutException:
            pass

        # Click bot app
        WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.CLASS_NAME, 'apps-list-item'))).click()

        # Go to resources
        time.sleep(2)
        driver.get(f"{driver.current_url}/resources")

        # Click edit to dyno
        WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.CLASS_NAME, 'clip')))
        buttons = driver.find_elements_by_tag_name("button")
        for button in buttons:
            if "dyno" in button.text:
                button.click()

        # Click toggle dyno
        driver.find_element_by_class_name("cmn-toggle").click()

        # Click confirm
        buttons = driver.find_elements_by_tag_name("button")
        for button in buttons:
            if "Confirm" in button.text:
                button.click()

        time.sleep(0.5)

        # Logout in order to login in the other account
        driver.get("https://dashboard.heroku.com/logout")
        i += 1


if __name__ == "__main__":
    main()