import time

from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def gen_element(by, value) -> dict:
    return {"by": by, "value": value}

NSS_URL = 'https://nsstools.austinisd.org/index.php'
NSS_USERNAME = gen_element(by=By.ID, value='username_input')
NSS_PASSWORD = gen_element(by=By.ID, value='password_input')
NSS_SIGN_IN_BUTTON = gen_element(by=By.ID, value='submit')
NSS_SIDE_MENU = gen_element(by=By.XPATH, value='//*[@id="accordionSidebar"]/li/a')
UNASSIGN_IPAD = gen_element(by=By.XPATH, value='//*[@id="collapse1"]/div/a[6]')
WIPE_CHECKBOX = gen_element(by=By.XPATH, value='//*[@id="wipeDeviceCheck"]')



def open_nss_site(driver: webdriver.Chrome, username: str, password: str) -> None:
    driver.get(NSS_URL)
    username_input = driver.find_element(**NSS_USERNAME)
    username_input.send_keys(username)
    password_intput = driver.find_element(**NSS_PASSWORD)
    password_intput.send_keys(password)
    sign_in = driver.find_element(**NSS_SIGN_IN_BUTTON)
    sign_in.click()
    side_menu = driver.find_element(**NSS_SIDE_MENU)
    side_menu.click()
    unassign_ipad = driver.find_element(**UNASSIGN_IPAD)
    unassign_ipad.click()     
    wipe_checkbox = driver.find_element(**WIPE_CHECKBOX)
    wipe_checkbox.click()

def wipe_ipad(driver: webdriver.Chrome | webdriver.Firefox | webdriver.Edge, SNorASSET: str) -> None:
    pass

# while True:
#     scan = input("Scan serial number or asset tag (0 to quit): ")
#     if scan == "0":
#         driver.close()
#         driver.quit()
#         break
#     if "-" in scan:
#         asset_tag_radio = driver.find_element(
#             by=By.XPATH, value='//*[@id="unassignipad_form"]/div[1]/label[1]/input'
#         )
#         asset_tag_radio.click()
#     else:
#         serial_number_radio = driver.find_element(
#             by=By.XPATH, value='//*[@id="unassignipad_form"]/div[1]/label[2]/input'
#         )
#         serial_number_radio.click()
#     input_field = driver.find_element(by=By.ID, value="deviceid")
#     input_field.send_keys(scan)
#     submit_button = driver.find_element(by=By.ID, value="submit_btn")
#     submit_button.click()
#     input_field.clear()
