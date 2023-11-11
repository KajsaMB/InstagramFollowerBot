from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from time import sleep
import os
from dotenv import load_dotenv
import random

load_dotenv("local.env")

driver = webdriver.Chrome(service=Service(executable_path="/Users/kajsa/Desktop/Development/chromedriver"))
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


class InstagramFollowerBot:

    def __init__(self, driver_path):
        # Selenium driver path
        self.driver = driver_path

    def login(self):
        # Opens instagram website and logs in to user account
        user = USERNAME
        password = PASSWORD
        self.driver.get("https://www.instagram.com/")
        sleep(2)
        self.driver.find_element(By.CLASS_NAME, "_a9_1").click()
        sleep(2)
        username_field = self.driver.find_element(By.NAME, "username")
        username_field.send_keys(user)
        sleep(1)
        password_field = self.driver.find_element(By.NAME, "password")
        password_field.send_keys(password)
        sleep(1)
        password_field.send_keys(Keys.ENTER)
        sleep(5)

    def find_followers(self, target_account):
        # Opens target account website, clicks on followers,
        # scrolls down the popup to load followers and passes popup to follow method.
        self.driver.get(f"https://www.instagram.com/{target_account}")
        sleep(4)
        self.driver.find_element(By.XPATH,
                                 "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a").click()
        sleep(2)
        popup = self.driver.find_element(By.XPATH,
                                         "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]")
        sleep(1)
        for i in range(10):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", popup)
            sleep(2)
        self.follow(popup)

    def follow(self, popup):
        # clicks on 'follow' buttons while also closing popups.
        follow_buttons = popup.find_elements(By.CSS_SELECTOR, "button")
        for button in follow_buttons:
            try:
                button.click()
            except ElementClickInterceptedException:
                try:
                    cancel_popup = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div["
                                                                      "2]/div/div/div[2]/div/div/div[1]/div/div["
                                                                      "2]/div/div/div/div/div[2]/div/div")
                    cancel_popup.find_element(By.CLASS_NAME, "_a9_1").click()
                    sleep(1)
                    button.click()
                except NoSuchElementException:
                    limit_popup = self.driver.find_element(By.XPATH,
                                                           "/html/body/div[1]/div/div/div/div[2]/div/div[2]/div["
                                                           "1]/div/div[2]/div/div/div/div/div[2]/div/div")
                    limit_popup.find_element(By.CLASS_NAME, "_a9_1").click()
                    print("Instagram auto limit reached 😩")
                    break
            except NoSuchElementException:
                limit_popup = self.driver.find_element(By.XPATH,
                                                       "/html/body/div[1]/div/div/div/div[2]/div/div[2]/div["
                                                       "1]/div/div[2]/div/div/div/div/div[2]/div/div")
                limit_popup.find_element(By.CLASS_NAME, "_a9_1").click()
                print("Instagram auto limit reached 😩")
                break
            finally:
                sleep(random.randint(1, 2))


target_account = "daviddoubilet"
bot = InstagramFollowerBot(driver)
bot.login()
bot.find_followers(target_account)
