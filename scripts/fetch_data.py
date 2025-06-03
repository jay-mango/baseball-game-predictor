from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.google.com")

print("Chrome opened. Waiting 5 seconds...")
time.sleep(5)

driver.quit()
print("Chrome closed.")
