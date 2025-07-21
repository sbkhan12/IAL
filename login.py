import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
# options.add_argument("--headless")  # Optional: headless mode
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 30)

username = 'your_username_here'  # Replace with your Instagram username
password = 'your_password_here'  # Replace with your Instagram password
target_username = ''

driver.get('https://www.instagram.com/accounts/login/')

wait.until(EC.presence_of_element_located((By.NAME, 'username'))).send_keys(username)
driver.find_element(By.NAME, 'password').send_keys(password + Keys.RETURN)

# Dismiss popups if appear
try:
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Not Now')]"))).click()
except:
    pass

try:
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Not Now')]"))).click()
except:
    pass

# Open user profile
driver.get(f'https://www.instagram.com/{target_username}/')
wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'/followers/')]"))).click()

# Scroll followers popup
time.sleep(2)
popup = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']//div[@role='dialog']")))

scroll_box = popup.find_element(By.XPATH, ".//div/div[2]")

for _ in range(10):  # Adjust scroll count as needed
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scroll_box)
    time.sleep(2)

followers = scroll_box.find_elements(By.XPATH, ".//li//div/div/div[2]/div[1]/div/span/a")

usernames = [follower.text for follower in followers if follower.text != '']

print(f"Total followers fetched: {len(usernames)}")

with open('followers_list.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Username'])
    for user in usernames:
        writer.writerow([user])

print("Followers saved to followers_list.csv")
driver.quit()
