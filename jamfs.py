import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By

JAMF_URL = 'https://login.jamfschool.com/login'


def open_jamf_site(driver: webdriver.Chrome, email: str, password: str) -> str:
    driver.get(JAMF_URL)
    driver_window_value: str = driver.current_window_handle
    jamf_email = driver.find_element(by="id",value="email")
    jamf_email.send_keys(email)
    jamf_password = driver.find_element(by="id", value="password")
    jamf_password.send_keys(password)
    sign_in = driver.find_element(by='xpath', value='//*[@id="app"]/div/div/article/div/div/form/div[3]/button')
    sign_in.click()
    side_menu = driver.find_element(by=By.XPATH, value='/html/body/div[2]/aside/section/ul/li[2]/a')
    side_menu.click()
    inventory_option = driver.find_element(by=By.XPATH, value='//*[@id="devices"]/li[1]/a')
    inventory_option.click()
    return driver_window_value

def update_jamf(driver: webdriver.Chrome, SNorASSET: str, school: str) -> None:
    inventory_search = driver.find_element(by=By.CSS_SELECTOR, value='input[placeholder="Search..."]')
    inventory_search.send_keys(SNorASSET)
    time.sleep(1.5)
    first_ipad = driver.find_element(by=By.XPATH, value='//*[@id="app"]/main/div/div[2]/div/div/table/tbody/tr/td[2]/div/div[2]/a')
    first_ipad.click()
    edit_details = driver.find_element(by=By.XPATH, value='//*[@id="details"]/div/div[1]/div/a')
    edit_details.click()
    change_button = driver.find_element(by=By.XPATH, value='//*[@id="toggle-move-to-location"]')
    change_button.click()
    driver.execute_script('document.getElementById("force-move-option-checkbox").click()')
    school_drop_down = Select(driver.find_element(by=By.ID, value='select-new-location'))
    school_drop_down.select_by_visible_text(text=school)
    save_details = driver.find_element(by=By.XPATH, value='//*[@id="modal-move-to-location-submit"]')
    save_details.click()
    save_ipad = driver.find_element(by=By.XPATH, value='//*[@id="btn-edit"]')
    save_ipad.click()
    side_menu = driver.find_element(by=By.XPATH, value='/html/body/div[2]/aside/section/ul/li[2]/a')
    side_menu.click()
    inventory_option = driver.find_element(by=By.XPATH, value='//*[@id="devices"]/li[1]/a')
    inventory_option.click()