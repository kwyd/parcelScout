#!/home/molang/scout/jeff_scout/bin/python3
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from pprint import pprint

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument('--disable-dev-shm-usage')
# Set a custom user agent to simulate different browsers or devices for enhanced stealth during automation
chrome_options.add_argument('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36')
chrome_options.headless = True # also works
#chrome_driver_path = './jeff_scout/lib/python3.11/site-packages/selenium/webdriver/chrome/'
chrome_driver_path = '/usr/bin/chromedriver'
driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_driver_path)

stealth(driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True)

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
  first, t_last = name.split("\t") 
  last = t_last.strip()
  for county in c_data:
    c_name, val_name, t_url = county.split("\t");
    url = t_url.strip()
    count += 1
 
    search_county_tax_sifter(url, val_name, last)
    time.sleep(5)
