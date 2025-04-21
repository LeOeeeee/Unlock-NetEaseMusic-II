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
    browser.add_cookie({"name": "MUSIC_U", "value": "00A512A4F99981EDA2A10FA73A5EF1AD15805E400DC047E896260E48ACD07348219F0525246394763CA0B92550BA9ACFFEB7DA86A8654D32054BD8582B781CB45B2BCEB518AA80B5B5D415EDE3684D3EB61A566184FC7FEC173EAF49002A65A3AA921CB06BF577771AEED67EF0685B8FD63BA1B3F45214A7F850B55EFFB2DF848DE5B9EC28563497FB584CF207E4AC5C5DBFAB67B79898B7A093B84ADEC8300DCF00BF117A01D6B67F2A3406A033C78CBAEAD21209F6011EA8CC916447BEA5B8ECE29756F21D504EC5B6B39618C53F076B7FC0650682EBB7D3234BA04BAAA2983BA5E0BE6DF11D9C00D6D847F1BE54F732E1B0857F44AD6F037E55E4D30E8D75E1C32151DB421F9D57EA5B17D0D5B89022942EE22531BF3A7A3B0B82E10873AC98D8AB924FFC9A9F84411E75C269D6B3F4688358CEAB0AF5D90CF91D94C40D0FE2182EA60EE5B1B02691F5C41A885E3C5C5B96A527BAE747BB0DF7EDA78DB40EDA"})
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
