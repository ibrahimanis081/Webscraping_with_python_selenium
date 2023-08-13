import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


# Create a new Chrome browser instance in headless mode and go to the URL
url = "https://oedb.org/accreditation/"
options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver.get(url)
total_page = 125

school_data_list = []

def scraper():
    # Wait for schools to be present
    schools = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[itemprop='name']"))
    )
    degree_levels = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[itemprop='itemOffered']"))
    )
    tuition_and_fees = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "dd[itemprop='makesOffer']"))
    )
    location = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[itemprop='addressLocality']"))
    )
    regions = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[itemprop='addressRegion']"))
    )
    school_types = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="hits-container"]/div/div[position() >= 1 and position() <= 20]/div/a/header/div/dl[3]/dd'))
    )
    
    for school, degree, fee, loc, reg, school_type in zip(schools, degree_levels, tuition_and_fees, location, regions, school_types):
        school_data = {
            'School': school.text,
            'Degree Level': degree.text,
            'Tuition and Fees': fee.text,
            'Location': loc.text,
            'Region': reg.text,
            'School Type': school_type.text
        }
        school_data_list.append(school_data)
    
    print(school_data_list)
    print(len(school_data_list))



if __name__ == '__main__':
    try:
        for _ in range(total_page):
            scraper()
            
            try:
                next_link = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "ais-pagination--link") and @aria-label="Next"]'))
                )
                next_link.click()
                print("Loading next page")
                time.sleep(10)
            except (NoSuchElementException, TimeoutException):
                print("No more 'Next' link found or timeout. Exiting loop.")
                break
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Finished")
    

with open("school_data.json", "w") as f:
    json.dump(school_data_list, f)


driver.quit()

