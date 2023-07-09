import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
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

def main() -> None:
    NSS_URL: str = 'https://nsstools.austinisd.org/index.php'

    NSS_USERNAME: dict = element_dict(by=By.ID,value="username_input")
    NSS_PASSWORD: dict = element_dict(by=By.ID,value="password_input")
    NSS_SIGN_IN_BUTTON: dict = element_dict(by=By.ID,value="submit")
    NSS_SIDE_MENU: dict = element_dict(by=By.XPATH,value='//*[@id="accordionSidebar"]/li/a')
    UNASSIGN_IPAD_OPTION: dict = element_dict(by=By.XPATH,value='//*[@id="collapse1"]/div/a[6]')
    WIPE_IPAD_CHECKBOX: dict = element_dict(by=By.XPATH,value='//*[@id="wipeDeviceCheck"]')
    ASSET_TAG_RADIO: dict = element_dict(by=By.XPATH,value='//*[@id="unassignipad_form"]/div[1]/label[1]/input')
    SERIAL_NUM_RADIO: dict = element_dict(by=By.XPATH,value='//*[@id="unassignipad_form"]/div[1]/label[2]/input')
    INPUT_FIELD: dict = element_dict(by=By.ID,value="deviceid")
    SUBMIT_BUTTON: dict = element_dict(by=By.ID,value="submit_btn")
    
    
    # ANSI escape characters for colors
    # Border color "Yellow"
    BC = "\033[0;33m"
    # Title color "Cyan"
    TC = "\033[0;36m"
    # Warning color "Red"
    WC = "\033[0;31m"
    # Color terminator
    CT = "\033[00m"
    
    print(
        f"""
    {BC}=============================={CT}
    {BC}|{CT}    {TC}NSSS auto wipe I-pad{CT}    {BC}|{CT}
    {BC}|{CT}                            {BC}|{CT}
    {BC}|{CT}  Created by: Darien Moore  {BC}|{CT}
    {BC}|{CT}============================{BC}|{CT}
    {BC}|{CT}   press Ctrl + C to exit.  {BC}|{CT}
    {BC}=============================={CT}"""
    )

    print(f"{SEPERATOR}\n")
    username: str = footer_input("Enter NSS username: ")
    password: str = footer_mask(prompt="Enter your NSS password: ")
    browser: str = footer_input(
        "Enter your desired browser (default: Chrome)\n 1. Chrome/Chromium, 2. Edge, 3. Firefox: ",
        depth=2,
    )
    minimized: str = footer_input("Start browser minimized? (defualt yes) y/n: ")
    if browser not in {"1", "2", "3"}:
        browser = "1"
    
    clear_lines(5)
    
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

    if minimized != "n".lower():
        driver.minimize_window()

    driver.implicitly_wait(35)

    driver.get(NSS_URL)

    footer_print("Logging in")
    driver.find_element(**NSS_USERNAME).send_keys(username)
    driver.find_element(**NSS_PASSWORD).send_keys(password)
    driver.find_element(**NSS_SIGN_IN_BUTTON).click()

    # TODO login failed check. need to be at work to test.

    footer_print('Opening "Unassign I-pad menu"')
    driver.find_element(**NSS_SIDE_MENU).click()
    driver.find_element(**UNASSIGN_IPAD_OPTION).click()
    driver.find_element(**WIPE_IPAD_CHECKBOX).click()
    Alert(driver=driver).accept()

    clear_lines(2)

    while True:
        scan: str = footer_input("Scan serial number or asset tag (0 to quit): ")
        if scan == "0":
            driver.close()
            driver.quit()
            break
        if "-" in scan:
            footer_print("Scanned asset tag")
            driver.find_element(**ASSET_TAG_RADIO).click()
        else:
            footer_print("Scanned serial number")
            driver.find_element(**SERIAL_NUM_RADIO).click()
        

        input_field = driver.find_element(**INPUT_FIELD)
        input_field.click()

        footer_print(f"Wiping I-pad:{scan}")
        driver.find_element(**SUBMIT_BUTTON).click()

        input_field.clear()

        clear_lines(4)

# ANSI escape characters to move terminal cursor
LINE_UP: str = "\033[1A"
LINE_DOWN: str = "\033[1B"
LINE_CLEAR: str = "\x1b[2K"
SEPERATOR: str = "-" * 38


# ANSI escape characters for colors
# Border color "Yellow"
BC = "\033[0;33m"
# Title color "Cyan"
TC = "\033[0;36m"
# Warning color "Red"
WC = "\033[0;31m"
# Color terminator
CT = "\033[00m"

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
    pass

if __name__ == "__main__":
    try:
        main()
    except TimeoutException:
        print("\n")
        print(
            f"{WC}Webpage took too long to load.{CT}\n{TC}Check internet connection and try agian.{CT}"
        )
    # TODO finish exceptions