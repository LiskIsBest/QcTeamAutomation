import time
import os
from dotenv import load_dotenv
load_dotenv()

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
JAMF_URL = 'https://login.jamfschool.com/login'
IPAD_ID = 'c121-33491'

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver: webdriver.Chrome = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(35)
print(driver.window_handles[0])

driver.get(JAMF_URL)
driver_window_value: str = driver.current_window_handle
# time.sleep(5)
print('clicking email form input')
jamf_email = driver.find_element(by=By.ID,value="email")
jamf_email.send_keys(email)
# time.sleep(0.2)

print('clicking password form input')
jamf_password = driver.find_element(by=By.ID, value="password")
jamf_password.send_keys(password)
# time.sleep(0.2)

print('clicking sign in')
sign_in = driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/div/article/div/div/form/div[3]/button')
sign_in.click()
# time.sleep(5)

print('opening devices drop menu')
side_menu = driver.find_element(by=By.XPATH, value='/html/body/div[2]/aside/section/ul/li[2]/a')
side_menu.click()
# time.sleep(1)

print('clicking inventory')
inventory_option = driver.find_element(by=By.XPATH, value='//*[@id="devices"]/li[1]/a')
inventory_option.click()
# time.sleep(20)

print("searching ipad")
inventory_search = driver.find_element(by=By.CSS_SELECTOR, value='input[placeholder="Search..."]')
inventory_search.send_keys(IPAD_ID)
time.sleep(1.5)

print("clicking ipad")
# link__2p2iH
first_ipad = driver.find_element(by=By.CLASS_NAME, value='link__2p2iH')
first_ipad.click()
# time.sleep(3)

print("clicking edit details")
edit_details = driver.find_element(by=By.XPATH, value='//*[@id="details"]/div/div[1]/div/a')
edit_details.click()
# time.sleep(3)

print("change location button")
change_button = driver.find_element(by=By.XPATH, value='//*[@id="toggle-move-to-location"]')
change_button.click()
# time.sleep(3)

print("turning on force now")
driver.execute_script('document.getElementById("force-move-option-checkbox").click()')
# time.sleep(2)

print("selecting dawson elementary")
school_drop_down = Select(driver.find_element(by=By.ID, value='select-new-location'))
school_drop_down.select_by_visible_text(text="Dawson Elementary")
# time.sleep(1.5)

print('saving details')
save_details = driver.find_element(by=By.XPATH, value='//*[@id="modal-move-to-location-submit"]')
save_details.click()
# time.sleep(3)

print('saving ipad')
save_ipad = driver.find_element(by=By.XPATH, value='//*[@id="btn-edit"]')
save_ipad.click()
# time.sleep(6)

print('opening devices drop menu')
side_menu = driver.find_element(by=By.XPATH, value='/html/body/div[2]/aside/section/ul/li[2]/a')
side_menu.click()
# time.sleep(1)

print('clicking inventory')
inventory_option = driver.find_element(by=By.XPATH, value='//*[@id="devices"]/li[1]/a')
inventory_option.click()
# time.sleep(20)