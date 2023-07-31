import json
import time
import logging
import re
import unittest
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoAlertPresentException,
    NoSuchElementException,
    InvalidSelectorException,
    TimeoutException,
)
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from seleniumwire import handler
import urllib.parse


class Tests(unittest.TestCase):
    def readJSONFile(self, filePath):
        with open(filePath, "r") as dataFile:
            data = json.load(dataFile)
        return data

    def setUp(self):
        options = webdriver.FirefoxOptions()
        profile = webdriver.FirefoxProfile()

        options.set_preference(
            "general.useragent.override",
            "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36 Edg/115.0.1901.188",
        )

        self.driver = webdriver.Firefox(options=options, firefox_profile=profile)

        self.driver.header_overrides = {
            "Sec-Ch-Ua": '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"'
        }

    def fetchBook(self):
        driver = self.driver

        driver.get("https://www.amazon.in/")

        # Read the JSON data from the file
        with open(
            "/path/to/file.json",
            "r",
        ) as json_file:
            books_data = json.load(json_file)

        for book_data in books_data:
            book_name = book_data["NAME of BOOKS"]
            author_name = book_data["AUTHOR"]

            search_query = f"{book_name} by {author_name}"

            input_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="nav-search-keywords"]')
                )
            )
            input_field.clear()
            input_field.send_keys(search_query)

            submit_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div[1]/header/div[1]/div[4]/form/div[2]/div/input",
                    )
                )
            )
            submit_button.click()

            try:
                image_src = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//img[@class='s-image']",
                        )
                    )
                )

                book_link = image_src.get_attribute("src")
                book_data["image_url"] = book_link


            except TimeoutException:
                book_data["image_url"] = None

        with open(
            "/path/to/file.json",
            "w",
        ) as json_file:
            json.dump(books_data, json_file)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(Tests("fetchBook"))
    unittest.TextTestRunner().run(suite)



# Sample json data

# [
#   {
#     "Barcode I D": 1,
#     "CALL NO": "624 PAT",
#     "NAME of BOOKS": "Elements of Civil Engineering",
#     "AUTHOR": "Patel J N & Gohil M B",
#     "PUBLISHERS": "Atul Prakashan, Ahmedabad",
#     "YEAR": 1999,
#     "Rec Date": "11.07.00",
#     "BILL NO": "1177/Roopal",
#     "PRICE": 150,
#     "ISBN": 0,
#     "BRANCH": "Civil",
#     "PAGE": 314,
#     "Dis": 30,
#     "Net Amt.": 120
#   },
#   {
#     "Barcode I D": 2,
#     "CALL NO": "510 SHA",
#     "NAME of BOOKS": "Engineering Mathematics",
#     "AUTHOR": "Sharma G S",
#     "PUBLISHERS": "CBS Publishers",
#     "YEAR": 1999,
#     "Rec Date": "11.07.00",
#     "BILL NO": "1177/Roopal",
#     "PRICE": 150,
#     "ISBN": 0,
#     "BRANCH": "Maths",
#     "PAGE": 90,
#     "Dis": 30,
#     "Net Amt.": 120
#   }
# ]
