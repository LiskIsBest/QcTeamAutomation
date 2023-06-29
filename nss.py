import time
import os
from dotenv import load_dotenv
load_dotenv()

from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(35)

print('opening nss tools')
driver.get('https://nsstools.austinisd.org/index.php')

print('entering username')
username_input = driver.find_element(by=By.ID, value='username_input')
username_input.send_keys(os.environ.get('USERNAME'))

print('entering password')
password_intput = driver.find_element(by=By.ID, value='password_input')
password_intput.send_keys(os.environ.get("PASSWORD"))

print('clicking sign in')
sign_in = driver.find_element(by=By.ID, value='submit')
sign_in.click()

side_menu = driver.find_element(by=By.XPATH, value='//*[@id="accordionSidebar"]/li/a')
side_menu.click()

unassign_ipad = driver.find_element(by=By.XPATH, value='//*[@id="collapse1"]/div/a[6]')
unassign_ipad.click()

wipe_checkbox = driver.find_element(by=By.XPATH, value='//*[@id="wipeDeviceCheck"]')
wipe_checkbox.click()

Alert(driver=driver).accept()
print('---------\n\n\n\n\n---------')

while(True):
    scan = input("Scan serial number or asset tag (0 to quit): ")
    if scan == '0':
        driver.close()
        driver.quit()
        break
    if '-' in scan:
        asset_tag_radio = driver.find_element(by=By.XPATH, value='//*[@id="unassignipad_form"]/div[1]/label[1]/input')
        asset_tag_radio.click()
    else:
        serial_number_radio = driver.find_element(by=By.XPATH, value='//*[@id="unassignipad_form"]/div[1]/label[2]/input')
        serial_number_radio.click()
    input_field = driver.find_element(by=By.ID, value='deviceid')
    input_field.send_keys(scan)
    submit_button = driver.find_element(by=By.ID, value='submit_btn')
    submit_button.click()
    input_field.clear()



