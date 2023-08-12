
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# Create a new Chrome browser instance and go to the URL
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get("https://oedb.org/accreditation/")


school_list = []
degree_levels_list = []
tuition_fees_list = []
location_list = []
regions_list = []
school_type_list = []

last_page = 125

def scraper():
    
    schools = driver.find_elements(By.CSS_SELECTOR, "span[itemprop='name']")
    for school in schools:
        school_list.append(school.text)
        del school_list[-1] # to remove the url of the webpage because it gets appended at end of list
        #print(school_list)
        print(len(school_list))
  

    degree_levels = driver.find_elements(By.CSS_SELECTOR, "span[itemprop='itemOffered']")
    for degree_level in degree_levels:
        degree_levels_list.append(degree_level.text)
    print(len(degree_levels_list))


    tuition_and_fees = driver.find_elements(By.CSS_SELECTOR, "dd[itemprop='makesOffer']")
    for fee in tuition_and_fees:
        tuition_fees_list.append(fee.text)
    print(len(tuition_fees_list))


    location = driver.find_elements(By.CSS_SELECTOR, "span[itemprop='addressLocality']")
    for locality in location:
        location_list.append(locality.text)
    print(len(location_list))


    regions = driver.find_elements(By.CSS_SELECTOR, "span[itemprop='addressRegion']")
    for region in regions:
        regions_list.append(region.text)
    print(len(regions_list))


    school_types = driver.find_elements(By.XPATH, '//*[@id="hits-container"]/div/div[position() >= 1 and position() <= 20]/div/a/header/div/dl[3]/dd')
    for school_type in school_types:
        school_type_list.append(school_type.text)
    print(len(school_type_list))
    
if __name__ == '__main__':
    scraper()
# next_link_xpath = driver.find_element(By.XPATH, '//a[contains(@class, "ais-pagination--link") and @aria-label="Next"]').click()
# scraper()

# for _ in range(5):
#     next_link_xpath = '//a[contains(@class, "ais-pagination--link") and @aria-label="Next"]'
#     next_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, next_link_xpath)))
#     next_link.click()
#     scraper()

# next_page = driver.find_element(By.XPATH, '//a[@aria-label="Next"]').click()

# for _ in range(last_page):
#     scraper()


# //*[@id="pagination-container"]/div/ul/li[8]/a

# <a class="ais-pagination--link" aria-label="Next" href="https://www.oedb.org/accreditation/?q=&amp;hPP=20&amp;idx=he_ipeds&amp;p=1&amp;dFR[distance_learning.online]=1">Next</a>






    
# //*[@id="pagination-container"]/div/ul/li[position() >= 1 and positin() <= 8]/a





#     # Add the extracted data to the list
#     data.append({
#         "school_name": school_name,
#         "degree_level": degree_level,
#         "tuition_fees": tuition_fees,
#         "location": location,
#         "school_type": school_type
#     })

# # Save the data to a JSON file
# with open("data.json", "w") as outfile:
#     json.dump(data, outfile)

# # Close the browser
# driver.quit()
