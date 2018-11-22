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
import random
import string

url = "https://omscentral.com/courses"
TABLE_NAME = "TABLE_REVIEWS"
rating_set = {"Strongly Disliked", "Disliked", "Neutral", "Liked", "Loved!"}
difficulty_set = {"Very Easy", "Easy", "Medium", "Hard", "Very Hard"}
workload_str = "hours/week"


class ScrapeOMSCentral:
    def __init__(self):
        self.driver = webdriver.Chrome("/Users/shwetasinghal/PycharmProjects/OMSCentralCrawler/venv/chromedriver")

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
            return "None"
        return text

    def get_random_word(self, length):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(length))

    def scrape_data(self):

        # course_table = driver.find_elements_by_css_selector("oms-course-list>div>table.mat-table>tbody>tr")
        self.wait = WebDriverWait(self.driver, 10)
        try:
            # wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, 'div.mat-select-value')))
            # driver.find_element_by_css_selector("div.mat-select-value").click()
            # driver.find_element_by_css_selector("#mat-option-24 > span").click()
            self.wait.until(expected_conditions.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'oms-course-list>div>table.mat-table>tbody>tr')))
            i = 1
            while i <= 51:
                try:
                    num_reviews = 0
                    self.driver.implicitly_wait(10)
                    course_table = self.driver.find_element_by_css_selector("oms-course-list>div>table.mat-table>tbody")
                    # driver.implicitly_wait(10)
                    self.wait.until(expected_conditions.element_to_be_clickable((
                        By.CSS_SELECTOR, "oms-course-list>div>table.mat-table>tbody>tr:nth-child(%s)" % i)))
                    course_name = course_table.find_element_by_css_selector(
                        "oms-course-list>div>table.mat-table>tbody>tr:nth-child(%s)>td" % i).text
                    course_table.find_element_by_css_selector(
                        "oms-course-list>div>table.mat-table>tbody>tr:nth-child(%s)" % i).click()
                    self.wait.until(
                        expected_conditions.presence_of_element_located((
                            By.CSS_SELECTOR,
                            'div> mat-list.mat-list > mat-list-item:nth-child(2) > div > div:nth-child(3)')))
                    num_reviews = self.driver.find_element_by_css_selector(
                        "div> mat-list.mat-list > mat-list-item:nth-child(2) > div > div:nth-child(3)").text

                    try:
                        self.wait.until(
                        expected_conditions.presence_of_element_located(
                            (By.CSS_SELECTOR, 'oms-course-reviews > div:nth-child(%s)' % num_reviews)))
                        reviews = self.driver.find_elements_by_css_selector("oms-course-reviews > div")
                    except Exception as e:
                        print e
                    j = 1
                    num_reviews = int(num_reviews.split(' ')[0])
                    while j != num_reviews + 1:
                        j = j + 1
                        try:
                            author = self.driver.find_element_by_css_selector(
                                "oms-course-reviews > div:nth-child(%s) > oms-review> mat-card>mat-card-subtitle.mat-card-subtitle > "
                                "span.ng-star-inserted" % j).text
                            if author is not "None":
                                author = author.split(': ')[1]
                            review_text = self.driver.find_element_by_css_selector(
                                "oms-course-reviews > div:nth-child(%s) > oms-review > mat-card > mat-card-content:nth-child(3)" % j).text
                            # self.wait.until(expected_conditions.presence_of_all_elements_located(
                            #     (By.CSS_SELECTOR, 'oms-course-reviews > div:nth-child(%s) > oms-review > mat-card > '
                            #                       'mat-card-content:nth-child(4) > mat-chip-list.mat-chip-list > div > mat-chip ' % j) ))
                            #
                            chip_list = self.driver.find_elements_by_css_selector("oms-course-reviews > div:nth-child(%s) > "
                                                                              "oms-review > mat-card > mat-card-content:nth-child(4) > "
                                                                              "mat-chip-list.mat-chip-list > div >mat-chip" % j)
                        # print chip_list
                            chips = []
                            for each in chip_list:
                                chips.append(each.text)
                        # chip1 = self.exists_element(
                        #     "oms-course-reviews > div:nth-child(%s) > oms-review > mat-card > mat-card-content:nth-child(4) > "
                        #     "mat-chip-list.mat-chip-list > div > mat-chip:nth-child(1)" % str(j))
                        # chip2 = self.exists_element(
                        #     "oms-course-reviews > div:nth-child(%s) > oms-review > mat-card > mat-card-content:nth-child(4) > "
                        #     "mat-chip-list.mat-chip-list > div > mat-chip:nth-child(2)" % j)
                        # chip3 = self.exists_element(
                        #     "oms-course-reviews > div:nth-child(%s) > oms-review > mat-card > mat-card-content:nth-child(4) > "
                        #     "mat-chip-list.mat-chip-list > div > mat-chip:nth-child(3)" % j)
                        # chip4 = self.exists_element(
                        #     "oms-course-reviews > div:nth-child(%s) > oms-review > mat-card > mat-card-content:nth-child(4) > "
                        #     "mat-chip-list.mat-chip-list > div > mat-chip:nth-child(4)" % j)
                        # chip5 = self.exists_element(
                        #     "oms-course-reviews > div:nth-child(%s) > oms-review > mat-card > mat-card-content:nth-child(4) > "
                        #     "mat-chip-list.mat-chip-list > div > mat-chip:nth-child(5)" % j)
                        # chips = [chip1, chip2, chip3, chip4, chip5]
                            rating = ""
                            difficulty = ""
                            workload = ""
                            for each in chips:
                                if each in rating_set:
                                    rating = each
                                if each in difficulty_set:
                                    difficulty = each
                                if workload_str in each:
                                    workload = each
                            values = (course_name, author, review_text, difficulty, rating, workload)
                            cnx.insert_into_table(TABLE_NAME, values)
                            print author
                            print review_text
                            print difficulty, ", ", rating, ", ", workload
                            # x = 0
                            # while x < 15:
                            #     author = self.get_random_word(25)
                            #     values = (course_name, author, review_text, difficulty, rating, workload)
                            #     cnx.insert_into_table(TABLE_NAME, values)
                            #     x = x + 1
                        except Exception as e:
                            print e

                except Exception as e:
                    print e
                    # self.driver.implicitly_wait(5)
                self.driver.execute_script("window.history.go(-1)")
                # self.driver.implicitly_wait(10)
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
