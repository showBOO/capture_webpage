import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
import traceback
import configparser
from datetime import datetime as dt
import glob
from PIL import Image
#import logging
from selenium.webdriver.remote.remote_connection import LOGGER
import requests

def main():

    # reading configuration file
    inifile = configparser.ConfigParser()
    inifile.read(os.path.dirname(__file__)+'./config.ini', 'UTF-8')

    # determin the save directory
    savetop = inifile['savetop']['dir']
    tdatetime = dt.now()
    savepath = savetop + '/' + tdatetime.strftime('%Y/%m/%d')+'/'
    os.makedirs(savepath, exist_ok=True)

    # logging setup
    #logging.basicConfig(filename=savepath + 'debug.log', level=logging.ERROR)

    url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'

    response = requests.get(url)

    # Webdriver options
    options = webdriver.ChromeOptions()

    # headless setting
    options.add_argument("start-maximized")
    options.add_argument("enable-automation")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument('--disable-extensions')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-gpu")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    # solved 'third-party cookie will be blocked. learn more in the issues tab'
    options.add_argument('log-level=3')
    prefs = {"profile.default_content_setting_values.notifications": 2}

    driver = webdriver.Chrome(options=options)

    with open('pages.txt') as f:
        pages = f.readlines()

    for page in pages:

        # adding set_page_load_timeout
        driver.set_page_load_timeout(30)

        print(page)

        try:

            driver.get(page)
            time.sleep(30)
            # w = driver.execute_script("return document.body.scrollWidth;")
            h = driver.execute_script("return document.body.scrollHeight;")
            driver.set_window_size(1920, h)

            # remove unnecessary line breaks
            fname = str(page).strip()
            # Remove characters that cannot be used in file names
            fname = fname.replace('/', '_').replace(':', '_').replace('?', '')

            driver.save_screenshot(savepath + fname + '.png')

        except TimeoutException as e:
            print("TimeoutException")

        except Exception as e:
            print(traceback.format_exc())

    driver.quit()

    # convert png to jpeg
    pngpath_list = glob.glob(savepath + '/*.png')  # get filelist of png files
    for pngpath in pngpath_list:
        basename = os.path.basename(pngpath)  # get filename
        # determin save filename
        save_filepath = savepath + basename[:-4] + '.jpg'
        img = Image.open(pngpath)
        img = img.convert('RGB')  # convert PNG to jpeg
        # jpeg parameter settings
        img.save(save_filepath, "JPEG", quality=80)
        if inifile['func']['is_del']:
            os.remove(pngpath)              # save as jpeg

if __name__ == '__main__':
    main()
