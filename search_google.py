#!/usr/local/nagios/libexec/python_web_checks/venv/bin/python3.8

#pip3 install selenium webdriver_manager marionette-driver marionette

from selenium.webdriver.common import by
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os, time


# Set environment variables
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''

def navigate(browser, SITE, PRINTP, delay):
    # Advanced buttom - //*[@id="advancedButton"]
    # Accept Risk and continue buttom - //*[@id="exceptionDialogButton"]

    try:
        browser.navigate(SITE)
    except Exception as e:
        # Handle firefox SSL Error
        if browser.find_element(By.XPATH, '//*[@id="advancedButton"]'):
            with open('/usr/local/nagios/libexec/python_web_checks/screenshot_firefox_SSL_ERROR.png', 'bw') as screenshot:
                browser.save_screenshot(fh=screenshot)
            print("Firefox SSL Error... Clicking in accept buttom ")
            browser.find_element(By.XPATH, '//*[@id="advancedButton"]').click()
            time.sleep(1)
            browser.find_element(By.XPATH, '//*[@id="exceptionDialogButton"]').click()
        else:
            print("CRITICAL: Load page failed!\n{}".format(e))
            with open('/usr/local/nagios/libexec/python_web_checks/screenshot_firefox_SSL_FAILURE.png', 'bw') as screenshot:
                browser.save_screenshot(fh=screenshot)
        try:
            browser.navigate(SITE)
        except Exception as e:
            print("CRITICAL: Load page failed! (2)\n{}".format(e))
            with open('/usr/local/nagios/libexec/python_web_checks/screenshot_load_page_google_ERROR.png', 'bw') as screenshot:
                browser.save_screenshot(fh=screenshot)
            exit(2)
        else:
            with open('/usr/local/nagios/libexec/python_web_checks/screenshot_load_page_google_OK.png', 'bw') as screenshot:
                browser.save_screenshot(fh=screenshot)

    try:
        WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH,'//html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input'))).send_keys("Python is cool!")

    except Exception as e:
        print("CRITICAL: URL Access Error! - {}".format(e))
        if PRINTP == True:
            with open('/usr/local/nagios/libexec/python_web_checks/screenshot_google_type_ERROR.png', 'bw') as screenshot:
                browser.save_screenshot(fh=screenshot)
        exit(2)
    else:
        if PRINTP == True:
            with open('/usr/local/nagios/libexec/python_web_checks/screenshot_google_type_OK.png', 'bw') as screenshot:
                browser.save_screenshot(fh=screenshot)

    try:
        browser.find_element(By.XPATH,'//html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)
        time.sleep(2)
    except Exception as e:
        print("CRITICAL: URL Access Error! - {}".format(e))
        if PRINTP == True:
            with open('/usr/local/nagios/libexec/python_web_checks/screenshot_google_hit_ENTER_ERROR.png', 'bw') as screenshot:
                browser.save_screenshot(fh=screenshot)
        exit(2)
    else:
        if PRINTP == True:
            with open('/usr/local/nagios/libexec/python_web_checks/screenshot_google_hit_ENTER_OK.png', 'bw') as screenshot:
                browser.save_screenshot(fh=screenshot)