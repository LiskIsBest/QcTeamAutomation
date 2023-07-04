import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By

def gen_element(by, value)->dict:
    return {
        'by': by,
        'value': value
    }
    

JAMF_URL = 'https://login.jamfschool.com/login'

JAMF_EMAIL = gen_element(by=By.ID, value='email')
JAMF_PASSWORD = gen_element(by=By.ID, value='password')
JAMF_SIGN_IN_BUTTON = gen_element(by=By.XPATH, value='//*[@id="app"]/div/div/article/div/div/form/div[3]/button')
DEVICES_SIDE_MENU = gen_element(by=By.XPATH, value='/html/body/div[2]/aside/section/ul/li[2]/a')
INVENTORY_OPTION = gen_element(by=By.XPATH, value='//*[@id="devices"]/li[1]/a')
INVENTORY_SEARCH = gen_element(by=By.CSS_SELECTOR, value='input[placeholder="Search..."]')
FIRST_IPAD_RESULT = gen_element(by=By.XPATH, value='//*[@id="app"]/main/div/div[2]/div/div/table/tbody/tr/td[2]/div/div[2]/a')
EDIT_DETAILS_BUTTON = gen_element(by=By.XPATH, value='//*[@id="details"]/div/div[1]/div/a')
LOCATION_CHANGE_BUTTON = gen_element(by=By.ID, value='toggle-move-to-location')
SCHOOL_LIST_DROP_DOWN = gen_element(by=By.ID, value='select-new-location')
SAVE_DETAILS_BUTTON = gen_element(by=By.ID, value='modal-move-to-location-submit')
SAVE_IPAD_BUTTON = gen_element(by=By.ID, value='btn-edit')

FORCE_MOVE_JAVASCRIPT = 'document.getElementById("force-move-option-checkbox").click()'


def open_jamf_site(driver: webdriver.Chrome, email: str, password: str) -> str:
    driver.get(JAMF_URL)
    driver_window_value: str = driver.current_window_handle
    jamf_email = driver.find_element(**JAMF_EMAIL)
    jamf_email.send_keys(email)
    jamf_password = driver.find_element(**JAMF_PASSWORD)
    jamf_password.send_keys(password)
    sign_in = driver.find_element(**JAMF_SIGN_IN_BUTTON)
    sign_in.click()
    side_menu = driver.find_element(**DEVICES_SIDE_MENU)
    side_menu.click()
    inventory_option = driver.find_element(**INVENTORY_OPTION)
    inventory_option.click()
    return driver_window_value


def update_jamf(driver: webdriver.Chrome, SNorASSET: str, school: str) -> None:
    inventory_search = driver.find_element(**INVENTORY_SEARCH)
    inventory_search.send_keys(SNorASSET)
    time.sleep(1.5)
    first_ipad = driver.find_element(**FIRST_IPAD_RESULT)
    first_ipad.click()
    edit_details = driver.find_element(**EDIT_DETAILS_BUTTON)
    edit_details.click()
    change_button = driver.find_element(**LOCATION_CHANGE_BUTTON)
    change_button.click()
    driver.execute_script(FORCE_MOVE_JAVASCRIPT)
    school_drop_down = Select(driver.find_element(**SCHOOL_LIST_DROP_DOWN))
    time.sleep(1.4)
    school_drop_down.select_by_visible_text(text=school)
    save_details = driver.find_element(**SAVE_DETAILS_BUTTON)
    save_details.click()
    save_ipad = driver.find_element(**SAVE_IPAD_BUTTON)
    save_ipad.click()
    side_menu = driver.find_element(**DEVICES_SIDE_MENU)
    side_menu.click()
    inventory_option = driver.find_element(**INVENTORY_OPTION)
    inventory_option.click()