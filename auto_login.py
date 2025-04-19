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
    browser.add_cookie({"name": "MUSIC_U", "value": "00E47A17A45A119A95BF61A33EDACF5DA62A2A509E4AB6C9969EF8430B86978DCB4BA2F1D986A17CE7140B32E06A804BC16E728A05C478F9717D2EB00A7C949B42A435EAB53C496F2F24FA24FC2704A9DF9630E02F19F77696F778508179BF8E443B49C743A3B6BCB1A2BEED7DBE0AAB5C891A79F28F91310E2A2AA8DEF35EC93947E550E542BE933DB9224883BE72370DC5B534B6FFBA3CDDBDB4C9CDA8F702E77DE56866A077344626D4D82944E99D8E89D279BA34193BA41648CFD5BD90D60DB5DF168B51374878028F9856588770073B79083F4BE727E26139596EF229DADF411527F3C08AD1EF2208B6EF3269A975B01D48B378D33E1DE634BA52176E39E79B09F62579C17AA7349E2CAE8BB0E6553FCEDD04BBC01816B0B502B689B40BC694638D46934C4AD34D7C8ACAD47494E1564228527DCA62BEEEC0DC0A1336FA82D026CE04A949D5BA2711F7C38988B78533AF980967DB851E0DEC65CEAF55F986"})
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
