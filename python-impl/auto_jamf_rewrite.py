import time
import os
from enum import Enum

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import (
    NoSuchWindowException,
    SessionNotCreatedException,
    ElementNotInteractableException,
    WebDriverException,
    TimeoutException,
    NoSuchElementException,
    ElementNotVisibleException,
)
from pick import pick
from urllib3.exceptions import ProtocolError
import maskpass


# ANSI escape characters for colors
# Border color "Yellow"
BC = "\033[0;33m"
# Title color "Cyan"
TC = "\033[0;36m"
# Warning color "Red"
WC = "\033[0;31m"
# Color terminator
CT = "\033[00m"

# ANSI escape characters to move terminal cursor
LINE_UP: str = "\033[1F"  # also moves cursor to beginning of line
LINE_DOWN: str = "\033[1B"
LINE_CLEAR: str = "\033[2K"
SEPERATOR: str = "-" * 38


class Browsers(Enum):
    CHROME = "1"
    EDGE = "2"
    FIREFOX = "3"


class AutoJamf:
    chromeOptions = ChromeOptions()
    chromeOptions.add_experimental_option("excludeSwitches", ["enable-logging"])
    edgeOptions = EdgeOptions()
    edgeOptions.add_experimental_option("excludeSwitches", ["enable-logging"])
    service = Service(log_path=os.path.devnull)  # for firefox
    default_wait = 30

    title_card = f"""
    {BC}=============================={CT}
    {BC}|{CT}  {TC}Jamf process automation{CT}   {BC}|{CT}
    {BC}|{CT}                            {BC}|{CT}
    {BC}|{CT}  Created by: Darien Moore  {BC}|{CT}
    {BC}|{CT}============================{BC}|{CT}
    {BC}|{CT}   press Ctrl + C to exit.  {BC}|{CT}
    {BC}=============================={CT}"""

    def __init__(self) -> None:
        print(f"{self.title_card}\n{SEPERATOR}\n")
        self.school: str = footer_input(
            "Enter the location name (check jamf for exact name): "
        )
        self.email: str = footer_input("Enter Jamf username/email: ")
        self.password: str = footer_mask(prompt="Enter your Jamf password: ")
        self.wipe: bool = (
            False
            if footer_input("Turn on the wipe functionality? (default Yes) Y/n: ")
            == "N".lower()
            else True
        )
        self.minimize: bool = (
            True
            if footer_input("Start browser minimized? (default No) y/n: ")
            == "Y".lower()
            else False
        )
        try:
            self.browser: Browsers = Browsers(
                footer_input(
                    "Enter your desired browser (default: Chrome)\n 1. Chrome/Chromium, 2. Edge, 3. Firefox: ",
                    depth=2,
                )
            )
        except:
            self.browser = Browsers.CHROME

        clear_lines(7)

        self.driver = self.open_browser(browser=self.browser)
        self.driver_handle = self.driver.current_window_handle

        clear_lines(self.login(email=self.email, password=self.password))

        while True:
            self.driver.implicitly_wait(self.default_wait)
            footer_print("Loading inventory")
            self.driver.find_element(**INVENTORY_SEARCH)
            clear_lines(1)

            scan = footer_input(" Scan serial number or asset tag (0 to quit): ")
            if scan == "0" or scan == "":
                self.driver.close()
                self.driver.quit()
                break

            lines_to_clear = self.process(scan=scan)
            clear_lines(lines_to_clear)

    def open_browser(
        self, browser: Browsers
    ) -> webdriver.Chrome | webdriver.Edge | webdriver.Firefox:
        match (browser):
            case Browsers.CHROME:
                driver = webdriver.Chrome(options=self.chromeOptions)
            case Browsers.EDGE:
                driver = webdriver.Edge(options=self.edgeOptions)
            case Browsers.FIREFOX:
                driver = webdriver.Firefox(service=self.service)
        driver.implicitly_wait(self.default_wait)

        if self.minimize:
            driver.minimize_window()

        return driver

    def login(self, email: str, password: str) -> int:
        self.driver.get(JAMF_URL)

        lines_to_clear: int = 2

        footer_print("Logging in")
        self.driver.find_element(**JAMF_EMAIL).send_keys(email)
        self.driver.find_element(**JAMF_PASSWORD).send_keys(password)
        self.driver.find_element(**JAMF_SIGN_IN_BUTTON).click()

        # Sign in failed check
        try:
            self.driver.implicitly_wait(5)
            self.driver.find_element(**JAMF_SIGN_IN_ERROR)
            raise SignInFailed
        except (NoSuchElementException, ElementNotVisibleException):
            pass

        # Authenticator code check
        try:
            self.driver.implicitly_wait(5)
            self.driver.find_element(**JAMF_AUTH_FORM)
            if isinstance(self.driver, webdriver.Firefox):
                self.driver.maximize_window()
            else:
                self.driver.switch_to.window(self.driver_handle)
            lines_to_clear += 2
            self.driver.implicitly_wait(60)
            footer_print(f"{TC}You have 60 seconds enter the authenticator code.{CT}")
            footer_print(
                f"{TC}Program will close if authenticator code is not entererd.{CT}"
            )
            try:
                self.driver.find_element(**DEVICES_SIDE_MENU)
            except TimeoutException:
                raise NoAuthCode
            self.driver.implicitly_wait(self.default_wait)
            if self.minimize:
                self.driver.minimize_window()
        except (NoSuchElementException, ElementNotVisibleException):
            pass

        footer_print('Opening "Devices/Inventory" menu')
        self.driver.get("https://austinisd.jamfcloud.com/devices")

        return lines_to_clear

    def process(self, scan: str) -> int:
        lines_to_clear: int = 11

        footer_print(f"Searching for I-pad:{scan}")
        inventory_search: WebElement = self.driver.find_element(**INVENTORY_SEARCH)
        inventory_search.clear()
        inventory_search.send_keys(scan)
        time.sleep(1.1)

        try:
            self.driver.implicitly_wait(2)
            self.driver.find_element(**FIRST_IPAD_RESULT).click()
            footer_print(f"Found I-pad:{scan}, clicking")
        except NoSuchElementException:
            footer_print(f"I-pad:{scan} not found. Returning to scan")
            time.sleep(3)
            return 3

        self.location_change()
        if self.wipe:
            lines_to_clear += 1
            self.wipe_user()

        footer_print("Saving I-pad")
        self.driver.find_element(**SAVE_IPAD_BUTTON).click()

        if self.wipe:
            lines_to_clear += 1
            self.erase_ipad(scan=scan)

        footer_print('Return to "Inventory" page')
        self.driver.find_element(**DEVICES_SIDE_MENU2)
        self.driver.get("https://austinisd.jamfcloud.com/devices")

        return lines_to_clear

    def location_change(self) -> None:
        footer_print('Opening "Edit details" menu')
        self.driver.find_element(**EDIT_DETAILS_BUTTON).click()

        footer_print('Clicking "Change" button')
        self.driver.find_element(**LOCATION_CHANGE_BUTTON).click()

        footer_print('Turning on "Force now"')
        self.driver.execute_script(FORCE_MOVE_JAVASCRIPT)

        footer_print(f"Selecting {self.school} from drop down")
        school_drop_down = Select(self.driver.find_element(**SCHOOL_LIST_DROP_DOWN))
        time.sleep(1.3)
        school_drop_down.select_by_visible_text(text=self.school)

        footer_print("Saving details")
        self.driver.find_element(**SAVE_DETAILS_BUTTON).click()

    def wipe_user(self) -> None:
        if self.driver.find_element(**USER_BOX).text == "":
            footer_print("No user to clear")
        else:
            footer_print("Clearing user")
            self.driver.find_element(**CURRENT_USER).click()

    def erase_ipad(self, scan: str) -> None:
        footer_print(f"Factory reseting I-pad:{scan}")
        self.driver.find_element(**ERASE_IPAD_BUTTON).click()
        self.driver.find_element(**ERASE_IPAD_CONFIRM).click()

    def shutdown(self) -> None:
        pass


class SignInFailed(Exception):
    pass


class NoAuthCode(Exception):
    pass


def element_dict(by: By | str = By.ID, value: str | None = None) -> dict:
    """generate dictionary with keyward args for "driver.find_element()"."""
    return {"by": by, "value": value}


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
    prints var:SEPERATOR below input() prompt.
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


def clear_lines(amount: int) -> None:
    """clear X lines above current terminal cursor location."""
    for _ in range(amount):
        print(LINE_UP, end=LINE_CLEAR)


JAMF_URL: str = "https://login.jamfschool.com/login"
FORCE_MOVE_JAVASCRIPT: str = (
    'document.getElementById("force-move-option-checkbox").click()'
)
JAMF_EMAIL: dict = element_dict(by=By.ID, value="email")
JAMF_PASSWORD: dict = element_dict(by=By.ID, value="password")
JAMF_SIGN_IN_BUTTON: dict = element_dict(
    by=By.XPATH, value='//*[@id="app"]/div/div/article/div/div/form/div[3]/button'
)
JAMF_SIGN_IN_ERROR: dict = element_dict(
    by=By.CLASS_NAME,
    value="error-text__29lYK",
)
JAMF_AUTH_FORM: dict = element_dict(
    by=By.XPATH, value='//*[@id="app"]/div/div/article/div/form/div[1]/div[2]/input'
)

DEVICES_SIDE_MENU: dict = element_dict(
    by=By.XPATH, value='//*[@id="app"]/aside/nav[1]/ul/li[2]/a'
)
DEVICES_SIDE_MENU2: dict = element_dict(
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
USER_BOX: dict = element_dict(by=By.XPATH, value='//*[@id="owner-id"]/option')
CURRENT_USER: dict = element_dict(by=By.CLASS_NAME, value="select2-selection__clear")

ERASE_IPAD_BUTTON: dict = element_dict(by=By.XPATH, value='//*[@id="importantButton"]')
ERASE_IPAD_CONFIRM: dict = element_dict(by=By.ID, value="wipe-submit")

LOCATION_CHANGE_BUTTON: dict = element_dict(by=By.ID, value="toggle-move-to-location")
SCHOOL_LIST_DROP_DOWN: dict = element_dict(by=By.ID, value="select-new-location")
SAVE_DETAILS_BUTTON: dict = element_dict(
    by=By.ID, value="modal-move-to-location-submit"
)
SAVE_IPAD_BUTTON: dict = element_dict(by=By.ID, value="btn-edit")


def main():
    try:
        AutoJamf()
    except TimeoutException:
        print("\n")
        print(
            f"{WC}Webpage took too long to load.{CT}\n{TC}Check internet connection and try agian.{CT}"
        )
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
            f"{WC}Browser was closed/crashed!{CT}\n{WC}Please do not close the browser while it is running.{CT}"
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


if __name__ == "__main__":
    main()
