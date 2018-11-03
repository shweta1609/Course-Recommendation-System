import requests
import re
import mysql
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from mysql import connector
from sql_conn import Conn

url = "https://omscentral.com/courses"
TABLE_NAME = "TABLE_REVIEWS"


class ScrapeOMSCentral:
    def __init__(self):
        self.driver = webdriver.Chrome("/Users/shwetasinghal/PycharmProjects/WebCrawlerBS/venv/chromedriver")

    def create_driver(self):
        self.driver.get(url)

    def close_driver(self):
        self.driver.close()

    def exists_element(self, locator):
        try:
            self.wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, locator)))
            text = self.driver.find_element_by_css_selector(locator).text
        except Exception as e:
            print e
            return None
        return text

    def scrape_data(self):
        self.driver.implicitly_wait(10)
        # course_table = driver.find_elements_by_css_selector("oms-course-list>div>table.mat-table>tbody>tr")
        self.wait = WebDriverWait(self.driver, 10)
        try:
            # wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, 'div.mat-select-value')))
            # driver.find_element_by_css_selector("div.mat-select-value").click()
            # driver.find_element_by_css_selector("#mat-option-24 > span").click()
            self.wait.until(expected_conditions.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'oms-course-list>div>table.mat-table>tbody>tr')))
            i = 1
            while i is not 11:
                course_table = self.driver.find_element_by_css_selector("oms-course-list>div>table.mat-table>tbody")
                # driver.implicitly_wait(10)
                self.wait.until(expected_conditions.element_to_be_clickable((
                    By.CSS_SELECTOR, "oms-course-list>div>table.mat-table>tbody>tr:nth-child(%s)" % i)))
                course_name = course_table.find_element_by_css_selector(
                    "oms-course-list>div>table.mat-table>tbody>tr:nth-child(%s)>td" % i).text
                course_table.find_element_by_css_selector(
                    "oms-course-list>div>table.mat-table>tbody>tr:nth-child(%s)" % i).click()
                self.wait.until(
                    expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, 'oms-course-reviews > div')))
                reviews = self.driver.find_elements_by_css_selector("oms-course-reviews > div")
                c = len(reviews)
                j = 1
                for each in reviews:
                    j = j + 1
                    author = self.exists_element(
                        "oms-course-reviews > div:nth-child(%s) > oms-review> mat-card>mat-card-subtitle.mat-card-subtitle > "
                        "span.ng-star-inserted" % j)
                    review_text = self.exists_element(
                        "oms-course-reviews > div:nth-child(%s) > oms-review > mat-card > mat-card-content:nth-child(3)" % j)
                    difficulty = self.exists_element(
                        "oms-course-reviews > div:nth-child(%s) > oms-review > mat-card > mat-card-content:nth-child(4) > "
                        "mat-chip-list.mat-chip-list > div > mat-chip:nth-child(2)" % j)
                    like = self.exists_element(
                        "oms-course-reviews > div:nth-child(%s) > oms-review > mat-card > mat-card-content:nth-child(4) > "
                        "mat-chip-list.mat-chip-list > div > mat-chip:nth-child(3)" % j)
                    workload = self.exists_element(
                        "oms-course-reviews > div:nth-child(%s) > oms-review > mat-card > mat-card-content:nth-child(4) > "
                        "mat-chip-list.mat-chip-list > div > mat-chip:nth-child(4)" % j)
                    values = (course_name, author, review_text, difficulty, like, workload)
                    cnx.insert_into_table(TABLE_NAME, values)
                    print author
                    print review_text
                    print difficulty, ", ", like, ", ", workload
                self.driver.implicitly_wait(5)
                self.driver.execute_script("window.history.go(-1)")
                self.driver.implicitly_wait(10)
                i = i + 1

        except Exception as e:
            print e


cnx = Conn()
cnx.create_database("DB_COURSE_REVIEWS")
cnx.create_table(TABLE_NAME)
scrape = ScrapeOMSCentral()
scrape.create_driver()
scrape.scrape_data()
scrape.close_driver()
cnx.close_conn()
