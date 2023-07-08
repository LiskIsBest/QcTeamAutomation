# title: auto_jamf.py
# author: Darien Moore
# github: https://github.com/LiskIsBest/QcTeamAutomation
# version: 1.0
# description: Automation of the I-pad location change inside of Jamf

import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FireOptions
from selenium.webdriver.firefox.service import Service as FireService
from selenium.common.exceptions import (
    NoSuchWindowException,
    SessionNotCreatedException,
    ElementNotInteractableException,
    WebDriverException,
    TimeoutException,
    NoSuchElementException,
    ElementNotVisibleException,
)
from urllib3.exceptions import ProtocolError
import maskpass

JAMF_URL: str = "https://login.jamfschool.com/login"
FORCE_MOVE_JAVASCRIPT: str = (
    'document.getElementById("force-move-option-checkbox").click()'
)

# ANSI escape characters for colors
# Border color "Yellow"
BC = "\033[0;33m"
# Title color "Cyan"
TC = "\033[0;36m"
# Warning color "Red"
WC = "\033[0;31m"
# Color terminator
CT = "\033[00m"


def main() -> None:
    JAMF_EMAIL: dict = element_dict(by=By.ID, value="email")
    JAMF_PASSWORD: dict = element_dict(by=By.ID, value="password")
    JAMF_SIGN_IN_BUTTON: dict = element_dict(
        by=By.XPATH, value='//*[@id="app"]/div/div/article/div/div/form/div[3]/button'
    )
    JAMF_SIGN_IN_ERROR: dict = element_dict(
        by=By.XPATH,
        value='//*[@id="app"]/div/div/article/div/div/form/div[2]/div[3]/small',
    )
    JAMF_AUTH_FORM: dict = element_dict(
        by=By.XPATH, value='//*[@id="app"]/div/div/article/div/form/div[1]/div[2]/input'
    )
    DEVICES_SIDE_MENU: dict = element_dict(
        by=By.CSS_SELECTOR, value='a[data-target="#devices"]'
    )
    INVENTORY_SEARCH: dict = element_dict(
        by=By.CSS_SELECTOR, value='input[placeholder="Search..."]'
    )
    FIRST_IPAD_RESULT: dict = element_dict(
        by=By.XPATH,
        value='//*[@id="app"]/main/div/div[2]/div/div/table/tbody/tr/td[2]/div/div[2]/a',
    )
    EDIT_DETAILS_BUTTON: dict = element_dict(
        by=By.XPATH, value='//*[@id="details"]/div/div[1]/div/a'
    )
    LOCATION_CHANGE_BUTTON: dict = element_dict(
        by=By.ID, value="toggle-move-to-location"
    )
    SCHOOL_LIST_DROP_DOWN: dict = element_dict(by=By.ID, value="select-new-location")
    SAVE_DETAILS_BUTTON: dict = element_dict(
        by=By.ID, value="modal-move-to-location-submit"
    )
    SAVE_IPAD_BUTTON: dict = element_dict(by=By.ID, value="btn-edit")

    print(
        f"""
    {BC}=============================={CT}
    {BC}|{CT}      {TC}Jamf auto update-{CT}     {BC}|{CT}
    {BC}|{CT}       {TC}I-pad location{CT}       {BC}|{CT}
    {BC}|{CT}                            {BC}|{CT}
    {BC}|{CT}  Created by: Darien Moore  {BC}|{CT}
    {BC}|{CT}============================{BC}|{CT}
    {BC}|{CT}   {WC}!Disable 2FA for Jamf!{CT}   {BC}|{CT}
    {BC}|{CT}  {WC}!Will not work otherwise!{CT} {BC}|{CT}
    {BC}|{CT}   press Ctrl + C to exit.  {BC}|{CT}
    {BC}=============================={CT}"""
    )

    print(f"{SEPERATOR}\n")
    school: str = footer_input("Enter the location name (check jamf for exact name): ")
    email: str = footer_input("Enter Jamf username/email: ")
    password: str = footer_mask(prompt="Enter your Jamf password: ")
    browser: str = footer_input(
        "Enter your desired browser (default: Chrome)\n 1. Chrome/Chromium, 2. Edge, 3. Firefox: ",
        depth=2,
    )
    minimized: str = footer_input("Start browser minimized? (defualt yes) y/n: ")
    if browser not in {"1", "2", "3"}:
        browser = "1"

    clear_lines(6)

    driver: webdriver.Chrome | webdriver.Edge | webdriver.Firefox
    match (browser):
        case "1":
            options = ChromeOptions()
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            driver = webdriver.Chrome(options=options)
        case "2":
            options = EdgeOptions()
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            driver = webdriver.Edge(options=options)
        case "3":
            options = FireOptions()
            service = FireService(log_path=os.path.devnull)
            driver = webdriver.Firefox(options=options, service=service)

    driver_handle = driver.current_window_handle

    if minimized != "n".lower():
        driver.minimize_window()

    driver.implicitly_wait(35)

    driver.get(JAMF_URL)

    lines_to_clear: int = 2

    footer_print("Logging in")
    driver.find_element(**JAMF_EMAIL).send_keys(email)
    driver.find_element(**JAMF_PASSWORD).send_keys(password)
    driver.find_element(**JAMF_SIGN_IN_BUTTON).click()

    # Sign in failed check
    try:
        driver.implicitly_wait(5)
        driver.find_element(**JAMF_SIGN_IN_ERROR)
    except (NoSuchElementException, ElementNotVisibleException):
        pass

    try:
        driver.implicitly_wait(5)
        driver.find_element(**JAMF_AUTH_FORM)
        if isinstance(driver, webdriver.Firefox):
            driver.maximize_window()
        else:
            driver.switch_to.window(driver_handle)
        lines_to_clear += 2
        driver.implicitly_wait(60)
        footer_print(f"{TC}You have 60 seconds enter the authenticator code.{CT}")
        footer_print(
            f"{TC}Program will close if authenticator code is not entererd.{CT}"
        )
        try:
            driver.find_element(**DEVICES_SIDE_MENU)
        except TimeoutException:
            raise NoAuthCode
        driver.implicitly_wait(35)
        if minimized != "n".lower():
            driver.minimize_window()
    except (NoSuchElementException, ElementNotVisibleException):
        pass

    footer_print('Opening "Devices/Inventory" menu')
    driver.get("https://austinisd.jamfcloud.com/devices")

    clear_lines(lines_to_clear)

    while True:
        footer_print("Loading inventory")
        inventory_search = driver.find_element(**INVENTORY_SEARCH)
        clear_lines(1)

        scan = footer_input(" Scan serial number or asset tag (0 to quit): ")
        if scan == "0" or scan == "":
            driver.close()
            driver.quit()
            break

        footer_print(f"Searching for I-pad:{scan}")
        inventory_search.clear()
        inventory_search.send_keys(scan)
        time.sleep(1.1)

        footer_print(f"Found I-pad:{scan}, clicking")
        driver.find_element(**FIRST_IPAD_RESULT).click()

        footer_print('Opening "Edit details" menu')
        driver.find_element(**EDIT_DETAILS_BUTTON).click()

        footer_print('Clicking "Change" button')
        driver.find_element(**LOCATION_CHANGE_BUTTON).click()

        footer_print('Turning on "Force now"')
        driver.execute_script(FORCE_MOVE_JAVASCRIPT)

        footer_print(f"Selecting {school} from drop down")
        school_drop_down = Select(driver.find_element(**SCHOOL_LIST_DROP_DOWN))
        time.sleep(1.3)
        school_drop_down.select_by_visible_text(text=school)

        footer_print("Saving details")
        driver.find_element(**SAVE_DETAILS_BUTTON).click()

        footer_print("Saving I-pad")
        driver.find_element(**SAVE_IPAD_BUTTON).click()

        footer_print(f"Updating I-pad:{scan} completed.")
        time.sleep(0.4)

        footer_print('Return to "Inventory" page')
        driver.find_element(**DEVICES_SIDE_MENU)
        driver.get("https://austinisd.jamfcloud.com/devices")

        clear_lines(11)


# ANSI escape characters to move terminal cursor
LINE_UP: str = "\033[1A"
LINE_DOWN: str = "\033[1B"
LINE_CLEAR: str = "\x1b[2K"
SEPERATOR: str = "-" * 38


def element_dict(by: By | str = By.ID, value: str | None = None) -> dict:
    """generate dictionary with keyward args for "driver.find_element()"."""
    return {"by": by, "value": value}


def clear_lines(amount: int) -> None:
    """clear X lines above current terminal cursor location."""
    for _ in range(amount):
        print(LINE_UP, end=LINE_CLEAR)


def footer_print(
    *args,
    **kwargs,
) -> None:
    """prints var:SEPERATOR below text printed."""
    clear_lines(1)
    print("\n" + SEPERATOR)
    print(LINE_UP * 2, *args, **kwargs)
    print(LINE_DOWN, end="")


def footer_input(prompt: str, depth: int = 1) -> str:
    """
    prints var:SEPERATOR below input() promt.
    rtype:str
    """
    clear_lines(1)
    print("\n" * depth + SEPERATOR)
    val = input(LINE_UP + LINE_UP * depth + prompt)
    print(LINE_DOWN, end="")
    return val


def footer_mask(prompt: str) -> str:
    """
    prints var:SEPERATOR below maskpass.askpass() prompt.
    rtype:str
    """
    clear_lines(1)
    print("\n" + SEPERATOR)
    val: str = maskpass.askpass(prompt=LINE_UP * 2 + prompt, mask="")
    print(LINE_DOWN, end="")
    return val


class SignInFailed(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class NoAuthCode(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


if __name__ == "__main__":
    try:
        main()
    except TimeoutException:
        print("\n")
        print(
            f"{WC}Webpage took too long to load.{CT}\n{TC}Check internet connection and try agian.{CT}"
        )
        pass
    except ElementNotInteractableException:
        print("\n")
        print(
            f"{WC}driver.find_element(**SOME_DATA) failed!\nContact program author.{CT}"
        )
    except SessionNotCreatedException:
        print("\n")
        print(
            f"{WC}Selected browser binary not found!\nPlease make sure the selected browser is installed.{CT}"
        )
    except ProtocolError:
        print("\n")
        print(f"{WC}Browser was closed before connecting to the first url!{CT}")
    except (NoSuchWindowException, WebDriverException):
        print("\n")
        print(
            f"{WC}Browser was closed!{CT}\n{WC}Please do not close the browser while it is running.{CT}"
        )
    except SignInFailed:
        print("\n")
        print(f"{WC}Sign in failed.\nEmail or Password were invalid.{CT}")
    except NoAuthCode:
        print("\n")
        print(f"{WC}Failed to enter your authenticator code in time.{WC}")
    except KeyboardInterrupt:
        print("\n")
        print(f"{TC}Ctrl+C pressed. Terminating program.{CT}")
    print("Closing in 8 seconds...")
    time.sleep(8)