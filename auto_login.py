# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00157E4C9EE2E443B238A78DBAA644375889779F9E47231DE069826850CC97505A0BEFA7B01A0DE085432A3FE4AFDB590E9AD75B83603C3764E3E41FFBABC25AE9C97F2836F9054DB9C8E60361FC7C80E38B60BFACDB564F37C178E163EA39070606FC8305F1863FA19B539302DB9CB363E35C93FD6DC96BC2DC5B70E050AF2F9CF02618CAABF977C7649DE2BDB31A1D4D8E4D7B3007D4FFA84BDDCC71DBC4C57D90266A24BE9799ACF55A9CBAA9305394D7518F98352A6517C872C3E833A8E9DD9E9D19B1377B8A551D4CF838E2A0B6C5DD68B7AF7F8A12E201AF9BFA975868A0D526FD5FD1998F5871C4B2C24BFD4BE509C7605E2F7D7B22F6077C6E498BE5DA872ADF04E98EDFF07F034A797B86E4E7E69BABE52AFB65D42E64A579007A427390FF1E223989CF174E19BF9DCC0EEFAC2143F0CE165D54E2048C45DD44166AA805832E9D6275C99A90C6DD60855F45390C755C1A6A427BB08808C03B3801C7C3"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
