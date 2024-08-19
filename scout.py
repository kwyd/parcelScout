#!/home/molang/scout/jeff_scout/bin/python3
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from pprint import pprint

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.headless = True # also works
chrome_driver_path = './jeff_scout/lib/python3.11/site-packages/selenium/webdriver'
service = ChromeService(chrome_driver_path)
driver = webdriver.Chrome(service)
pprint(driver)
def search_county_tax_sifter(url, value_name, search_string):

    driver.get(url)
    
    try:
        # Wait for the "I understand" button to be clickable and click it
        wait = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "cphContent_btnAgree"))).click()
 
        # Find the search input field and submit the property address
        search_input = driver.find_element(By.NAME, value_name)
        search_input.send_keys(search_string)
        time.sleep(5)
        search_input.submit()
 
        # Wait for the search results to load
        wait = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "result")))
 
        # Extract and print the search results using BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        search_results = soup.find_all("div", class_="result")
        for result in search_results:
            address = result.find("div", class_="details").text.strip()
            owner_name = result.find("div", class_="nav").text.strip()
            print("Address:", address)
            print("Owner:", owner_name)
            print()
    except Exception as e:
        print("An error occurred:", e)
    finally:
        driver.quit()
 
lines = open('t_counties.txt', 'r')
c_data = lines.readlines()
 
legislators = open('t_legs.txt', 'r')
l_data = legislators.readlines()
 
count = 0
 
for name in l_data:
  first, tlast = name.split("\t") 
  last = tlast.strip()
  for county in c_data:
    c_name, val_name, url = county.split("\t");
    count += 1
    print(c_name, last)
 
# Example usage:
    print(last, url, c_name, sep=" ");
    search_county_tax_sifter(url, val_name, last)
    time.sleep(5)
