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
LINE_UP: str = "\033[1F" # also moves cursor to beginning of line
LINE_DOWN: str = "\033[1B"
LINE_CLEAR: str = "\033[2K"
SEPERATOR: str = "-" * 38


class AutoJamf:
    options = ChromeOptions()  # for chromium
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    service = FireService(log_path=os.path.devnull)  # for firefox

    title_card = f"""
    {BC}=============================={CT}
    {BC}|{CT}      {TC}Jamf auto update-{CT}     {BC}|{CT}
    {BC}|{CT}       {TC}I-pad location{CT}       {BC}|{CT}
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
        self.browser: str = footer_input(
            "Enter your desired browser (default: Chrome)\n 1. Chrome/Chromium, 2. Edge, 3. Firefox: ",
            depth=2,
        )

    def login(self, email: str, password: str) -> None:
        pass

    def location_change(self, school: str = "Austin Independent School Dist") -> None:
        pass

    def wipe_ipad(self) -> None:
        pass

    def shutdown(self) -> None:
        pass


def footer_print(
    *args,
    **kwargs,
) -> None:
    """prints var:SEPERATOR below text printed."""
    print(LINE_UP + LINE_CLEAR, *args, **kwargs)
    print(SEPERATOR)


def footer_input(prompt: str, depth: int = 1) -> str:
    """
    prints var:SEPERATOR below input() prompt.
    rtype:str
    """
    print(LINE_UP + LINE_CLEAR + "\n" * depth + SEPERATOR, end="")
    val = input(LINE_UP * depth + prompt)
    print(LINE_DOWN, end="")
    return val


def footer_mask(prompt: str) -> str:
    """
    prints var:SEPERATOR below maskpass.askpass() prompt.
    rtype:str
    """
    print(LINE_UP + LINE_CLEAR + "\n" + SEPERATOR, end="")
    val: str = maskpass.askpass(prompt=LINE_UP + prompt, mask="")
    print(LINE_DOWN, end="")
    return val


def clear_lines(amount: int) -> None:
    """clear X lines above current terminal cursor location."""
    for _ in range(amount):
        print(LINE_UP, end=LINE_CLEAR)


def main():
    AutoJamf()
    pass


if __name__ == "__main__":
    main()
