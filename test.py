from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
import time
import json

# Create a new Chrome browser instance and go to the URL
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get("https://oedb.org/accreditation/")
driver.maximize_window()

WebDriverWait(driver, 20)



# schools = driver.find_elements(By.CSS_SELECTOR, "span[itemprop='name']")
for _ in range(10):
    next_pages = driver.find_element(By.LINK_TEXT, "Next").click()
    WebDriverWait(driver, 20)

# //*[@id="pagination-container"]/div/ul/li[6]/a
# //*[@id="pagination-container"]/div/ul/li[3]/a
# //*[@id="pagination-container"]/div/ul/li[4]/a
# WebDriverWait(driver, 20)
# driver.quit()


