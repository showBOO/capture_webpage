import os
import time
from selenium import webdriver
import configparser
from datetime import datetime as dt


def main():

    inifile = configparser.ConfigParser()
    inifile.read('./config.ini', 'UTF-8')

    savetop = inifile['savetop']['dir']
    tdatetime = dt.now()
    savepath = savetop + '/' + tdatetime.strftime('%Y/%m/%d')+'/'
    os.makedirs(savepath, exist_ok=True)

    # Webdriver options
    options = webdriver.ChromeOptions()

    # headless
    options.add_argument('--headless')
    options.add_argument("--disable-hang-monitor")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(
        "C:\\webdriver\\chromedriver.exe", options=options)

    with open('pages.txt') as f:
        pages = f.readlines()

    for page in pages:

        driver.get(page)
        time.sleep(3)
        # w = driver.execute_script("return document.body.scrollWidth;")
        h = driver.execute_script("return document.body.scrollHeight;")
        driver.set_window_size(1920, h)

        # remove unnecessary line breaks
        fname = str(page).strip()
        # Remove characters that cannot be used in file names
        fname = fname.replace('/', '_').replace(':', '_').replace('?', '')

        driver.save_screenshot(savepath + fname + '.png')

    driver.quit()


if __name__ == '__main__':
    main()
