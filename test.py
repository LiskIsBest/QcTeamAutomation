import time
import os
from dotenv import load_dotenv
load_dotenv()

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By

email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
JAMF_URL = 'https://login.jamfschool.com/login'
# IPAD_ID = 'c121-33491'

chrome_options = ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver: webdriver.Chrome = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(35)

driver.get(JAMF_URL)
driver_window_value: str = driver.current_window_handle
print('clicking email form input')
jamf_email = driver.find_element(by=By.ID,value="email")
jamf_email.send_keys(email)

print('clicking password form input')
jamf_password = driver.find_element(by=By.ID, value="password")
jamf_password.send_keys(password)

print('clicking sign in')
sign_in = driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/div/article/div/div/form/div[3]/button')
sign_in.click()

print('opening devices drop menu')
side_menu = driver.find_element(by=By.XPATH, value='/html/body/div[2]/aside/section/ul/li[2]/a')
side_menu.click()

print('clicking inventory')
inventory_option = driver.find_element(by=By.XPATH, value='//*[@id="devices"]/li[1]/a')
inventory_option.click()

print()
school = input("Enter school name: ")
print('----------\n\n\n----------')

while(True):
    print('Ready to scan...')
    scan = input("Scan serial number or asset tag (0 to quit): ")
    if scan == '0':
        driver.close()
        driver.quit()
        break

    print("searching ipad")
    inventory_search = driver.find_element(by=By.CSS_SELECTOR, value='input[placeholder="Search..."]')
    inventory_search.clear()
    inventory_search.send_keys(scan)
    time.sleep(1.4)

    print("clicking ipad")
    first_ipad = driver.find_element(by=By.CLASS_NAME, value='link__2p2iH')
    first_ipad.click()

    print("clicking edit details")
    edit_details = driver.find_element(by=By.XPATH, value='//*[@id="details"]/div/div[1]/div/a')
    edit_details.click()

    print("change location button")
    change_button = driver.find_element(by=By.XPATH, value='//*[@id="toggle-move-to-location"]')
    change_button.click()

    print("turning on force now")
    driver.execute_script('document.getElementById("force-move-option-checkbox").click()')

    print(f"selecting {school}")
    school_drop_down = Select(driver.find_element(by=By.ID, value='select-new-location'))
    time.sleep(1.4)
    school_drop_down.select_by_visible_text(text=school)

    print('saving details')
    save_details = driver.find_element(by=By.XPATH, value='//*[@id="modal-move-to-location-submit"]')
    save_details.click()

    print('saving ipad')
    save_ipad = driver.find_element(by=By.XPATH, value='//*[@id="btn-edit"]')
    save_ipad.click()

    print('opening devices drop menu')
    side_menu = driver.find_element(by=By.XPATH, value='/html/body/div[2]/aside/section/ul/li[2]/a')
    side_menu.click()

    print('clicking inventory')
    inventory_option = driver.find_element(by=By.XPATH, value='//*[@id="devices"]/li[1]/a')
    inventory_option.click()
    time.sleep(2)

    inventory_search = driver.find_element(by=By.CSS_SELECTOR, value='input[placeholder="Search..."]')
    inventory_search.clear()