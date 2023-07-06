import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FoxOptions
import maskpass

#  line up, clear, debug info, next line print break line

# IPAD_ID = 'c121-33491'
LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'

def gen_element(by, value) -> dict:
    return {'by': by, 'value': value}

def clear_lines(amount: int):
    for i in range(amount):
        print(LINE_UP, end=LINE_CLEAR)

JAMF_EMAIL = gen_element(by=By.ID, value='email')
JAMF_PASSWORD = gen_element(by=By.ID, value='password')
JAMF_SIGN_IN_BUTTON = gen_element(by=By.XPATH, value='//*[@id="app"]/div/div/article/div/div/form/div[3]/button')
DEVICES_SIDE_MENU = gen_element(by=By.CSS_SELECTOR, value='a[data-target="#devices"]')
INVENTORY_OPTION = gen_element(by=By.XPATH, value='//*[@id="devices"]/li[1]/a')
INVENTORY_SEARCH = gen_element(by=By.CSS_SELECTOR, value='input[placeholder="Search..."]')
FIRST_IPAD_RESULT = gen_element(by=By.XPATH,value='//*[@id="app"]/main/div/div[2]/div/div/table/tbody/tr/td[2]/div/div[2]/a',)
EDIT_DETAILS_BUTTON = gen_element(by=By.XPATH, value='//*[@id="details"]/div/div[1]/div/a')
LOCATION_CHANGE_BUTTON = gen_element(by=By.ID, value='toggle-move-to-location')
SCHOOL_LIST_DROP_DOWN = gen_element(by=By.ID, value='select-new-location')
SAVE_DETAILS_BUTTON = gen_element(by=By.ID, value='modal-move-to-location-submit')
SAVE_IPAD_BUTTON = gen_element(by=By.ID, value='btn-edit')

JAMF_URL = 'https://login.jamfschool.com/login'
FORCE_MOVE_JAVASCRIPT = 'document.getElementById("force-move-option-checkbox").click()'

print("""
==============================
|      Jamf auto update-     |
|       I-pad location       |
|                            |
|  Created by: Darien Moore  |
==============================
""")
school = input('Enter the location name (check jamf for exact name): ')
email = input('Enter Jamf username/email: ')
password = maskpass.askpass(prompt='Enter your Jamf password: ',mask='')
browser = input('Enter your desired browser.\n(default: Chrome) 1. Chrome/Chromium, 2. Edge, 3. Firefox: ')
minimized = input('Start browser minimized? (defualt yes) y/n: ')
if browser not in {'1','2','3'}:
    browser = '1'

clear_lines(6)

match(browser):
    case '1':
        options = ChromeOptions()
        driver: webdriver.Chrome = webdriver.Chrome(options=options)
    case '2':
        options = EdgeOptions()
        driver: webdriver.Edge = webdriver.Edge(options=options)
    case '3':
        options = FoxOptions()
        driver: webdriver.Firefox = webdriver.Firefox(options=options)
if minimized != 'n'.lower():
    driver.minimize_window()
driver.implicitly_wait(35)

driver.get(JAMF_URL)

print('\nLogging in...')
driver.find_element(**JAMF_EMAIL).send_keys(email)
driver.find_element(**JAMF_PASSWORD).send_keys(password)
driver.find_element(**JAMF_SIGN_IN_BUTTON).click()

print('opening "Devices"')
driver.find_element(**DEVICES_SIDE_MENU)
driver.get('https://austinisd.jamfcloud.com/devices')

# print('clicking inventory')
# driver.find_element(**INVENTORY_OPTION).click()

clear_lines(2)

while(True):
    print('Wait for the search page to load before scanning.')
    scan = input("Scan serial number or asset tag (0 to quit): ")
    if scan == '0' or scan == '':
        driver.close()
        driver.quit()
        break

    print("searching ipad")
    inventory_search = driver.find_element(**INVENTORY_SEARCH)
    inventory_search.clear()
    inventory_search.send_keys(scan)
    time.sleep(1.4)

    print("clicking ipad")
    driver.find_element(**FIRST_IPAD_RESULT).click()

    print("clicking edit details")
    driver.find_element(**EDIT_DETAILS_BUTTON).click()

    print("change location button")
    driver.find_element(**LOCATION_CHANGE_BUTTON).click()

    print("turning on force now")
    driver.execute_script(FORCE_MOVE_JAVASCRIPT)

    print(f"selecting {school}")
    school_drop_down = Select(driver.find_element(**SCHOOL_LIST_DROP_DOWN))
    time.sleep(1.4)
    school_drop_down.select_by_visible_text(text=school)

    print('saving details')
    driver.find_element(**SAVE_DETAILS_BUTTON).click()

    print('saving ipad')
    driver.find_element(**SAVE_IPAD_BUTTON).click()

    print('opening devices drop menu')
    # driver.find_element(**DEVICES_SIDE_MENU).click()
    driver.find_element(**DEVICES_SIDE_MENU)
    driver.get('https://austinisd.jamfcloud.com/devices')

    # print('clicking inventory')
    # driver.find_element(**INVENTORY_OPTION).click()
    # time.sleep(1)
    print(f'Updating I-pad:{scan} completed.')
    time.sleep(1)
