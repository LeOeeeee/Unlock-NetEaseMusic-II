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
    browser.add_cookie({"name": "MUSIC_U", "value": "0040BE3BB4F733B7BE0EB116DA59A9256A6D4BA4AC76B9C38B1CD87D33D069E9C121324AB9B6CF07A4D32C446A753F906F44A0EE1DCC1905822257C5C60542475400ECD6ADDD85980FB0AF21F53269984213182838FF0A60F0827DDC0796377F1A418133D151A6AAFF0DE0BADFDF21B4A3EFCA0FC53C7D54648067B869D93974ADA1888256A9BBA3EFCFB136DA10B54AE84940CC90A5F2DB63F565AFF93B17106D57C5C9C81547E0731046F80D5F24AEA03670050D0605888B41731421F855D7EE6487D7A82290899C09038D9D7CEFA588D5A9B10E1A85D18B2734BC55241B0D0A2A808E7B24A8B161F96C4092C34A498B708AA0E05D90A4F94ACFE6F03EC2740F51F53E1EF6FA41A7ABC6A975A382CF15B2214AF2BEBE3B961BA302AF78FFB7D29484CC1D684DEC4E8750E977AE634C4A59F2C7641F2A2F040BD4E733AD53A61D27981F83B9D05EA494646A0B17D36A7383FF454AF995444F2E2EFC48FAC618E8"})
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
