import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By


def gen_element(by, value) -> dict:
    return {"by": by, "value": value}


JAMF_URL = "https://login.jamfschool.com/login"

JAMF_EMAIL = gen_element(by=By.ID, value="email")
JAMF_PASSWORD = gen_element(by=By.ID, value="password")
JAMF_SIGN_IN_BUTTON = gen_element(
    by=By.XPATH, value='//*[@id="app"]/div/div/article/div/div/form/div[3]/button'
)
DEVICES_SIDE_MENU = gen_element(
    by=By.XPATH, value="/html/body/div[2]/aside/section/ul/li[2]/a"
)
INVENTORY_OPTION = gen_element(by=By.XPATH, value='//*[@id="devices"]/li[1]/a')
INVENTORY_SEARCH = gen_element(
    by=By.CSS_SELECTOR, value='input[placeholder="Search..."]'
)
FIRST_IPAD_RESULT = gen_element(
    by=By.XPATH,
    value='//*[@id="app"]/main/div/div[2]/div/div/table/tbody/tr/td[2]/div/div[2]/a',
)
EDIT_DETAILS_BUTTON = gen_element(
    by=By.XPATH, value='//*[@id="details"]/div/div[1]/div/a'
)
LOCATION_CHANGE_BUTTON = gen_element(by=By.ID, value="toggle-move-to-location")
SCHOOL_LIST_DROP_DOWN = gen_element(by=By.ID, value="select-new-location")
SAVE_DETAILS_BUTTON = gen_element(by=By.ID, value="modal-move-to-location-submit")
SAVE_IPAD_BUTTON = gen_element(by=By.ID, value="btn-edit")

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


JAMF_SCHOOLS = [
    "Austin Independent School Dist",
    "ACADEMICS",
    "ACCOUNTABILITY/PEIMS",
    "ADVANCED ACADEMICS",
    "AISD JAMF School Main",
    "AISD Meraki",
    "AISD Technology",
    "AISDCDC (Austin ISD Child Dev Ctr)",
    "Akins High",
    "Akins HS",
    "Allison Elementary",
    "ALTERNATIVE EDUCATION",
    "Alternative Learning Center",
    "Alternative Learning Center",
    "Anderson High",
    "Anderson HS",
    "Andrews Elementary",
    "ANITA FERRALES COY FACILITY",
    "Ann Richards",
    "Ann Richards 2",
    "ASSOC SUPT-ACADEMICS & SEL",
    "ASSOC SUPT-AREA 1",
    "ASSOC SUPT-ELEM SCHOOLS",
    "ASSOC SUPT-HIGH SCHOOLS",
    "ASSOC SUPT-MIDDLE SCHOOLS",
    "ATHLETICS",
    "Austin High",
    "Austin HS",
    "Austin State Hospital",
    "AVID COLLEGE READINESS",
    "Bailey Middle",
    "Bailey MS",
    "Baldwin Elementary",
    "Baranoff Elementary",
    "Barrington Elementary",
    "Barton Hills Elementary",
    "Bear Creek Elementary",
    "Becker Elementary",
    "Bedichek Middle",
    "Bedichek MS",
    "BENEFITS OFFICE",
    "Bilingual",
    "Blackshear Elementary",
    "Blanton Elementary",
    "Blazier Elementary",
    "BOARD OF TRUSTEES",
    "Boone Elementary",
    "Bowie High",
    "Bowie HS",
    "Brentwood Elementary",
    "Brooke Elementary",
    "Brown Elementary",
    "Bryker Woods Elementary",
    "BUDGET",
    "Burger Activity Center",
    "Burnet Middle",
    "Burnet MS",
    "Burnet MS 2",
    "CABLE TV/AMPS",
    "Campbell Elementary",
    "CAMPUS/DISTRICT ACCOUNTABILITY",
    "CAREER AND TECH EDUCATION",
    "Casey Elementary",
    "Casis Elementary",
    "CATE",
    "CATE 2",
    "CENTRAL WAREHOUSE",
    "Cheif Schools Office",
    "CHIEF FINANCIAL OFFICER",
    "CHIEF HUMAN CAPITAL OFFICER",
    "CHILD STUDY SYSTEMS",
    "Clayton Elementary",
    "Clifton Career Dev. School 2",
    "CLIFTON CENTER",
    "COMM ED-AFT SCH PROG",
    "COMMUNITY EDUCATION-SOUTH",
    "CONSTRUCTION MANAGEMENT",
    "Contract & Procurement Services",
    "Contract & Procurement Services",
    "Cook Elementary",
    "Covington Middle",
    "Covington MS",
    "Cowan Elementary",
    "CREATIVE LEARNING INITIATIVE",
    "Crockett Early College HS",
    "Crockett High",
    "Cunningham Elementary",
    "Cunningham Elementary School 2",
    "CUSTOMER SUPPORT SRVCS",
    "Davis Elementary",
    "Dawson Elementary",
    "DCCE",
    "DCMC Education Center",
    "Delco Activity Center",
    "Dell PHP",
    "DISTRICT POLICE",
    "Dobie Middle",
    "Dobie MS",
    "DOBIE PRE-K CENTER",
    "Doss Elementary",
    "DYSLEXIA 504 PROGRAM",
    "DYSLEXIA/504 PROGRAM",
    "EARLY CHILDHOOD",
    "Eastside Memorial Early College HS",
    "Eastside Memorial HS at Johnston",
    "EDAEP",
    "EDUCATION SUPPORT SERVICES",
    "Education Support Services",
    "Educator Quality",
    "Educator Quality 2",
    "ELEMENTARY MUSIC",
    "FERRALES COY FACILITY",
    "Finance",
    "FINANCE",
    "FOOD SERVICE",
    "Galindo Elementary",
    "GARCIA MIDDLE",
    "Garcia YMLA",
    "Garcia YMLA",
    "Garza Independence High",
    "Garza Independent HS",
    "Gorzycki Middle",
    "Gorzycki MS",
    "Govalle Elementary",
    "Graduation Prep Academy @ Lanier",
    "Graduation Prep Academy @ Lanier 2",
    "Graduation Prep Academy @ Travis",
    "Graduation Prep Academy at Navarro",
    "GRADUATION PREPARATORY ACADEMY",
    "Graduation Preparatory Academy",
    "Graham Elementary",
    "GRANT DEV & PROG SPPRT/NOVANET",
    "Guerrero-Thompson Elem",
    "Gullett Elementary",
    "Harris Elementary",
    "Hart Elementary",
    "HEALTH SERVICES",
    "Health Services",
    "High School Office",
    "Highland Park Elementary",
    "Hill Elementary",
    "HISTORICALLY UNDERUTILIZED BUSINESSES",
    "HOMEBOUND",
    "House Park",
    "Houston Elementary",
    "HUMAN RESOURCE SERVICES",
    "HUMANITIES",
    "HUSTON-TILLOTSON",
    "INFORMATION SYSTEM ADMIN",
    "INFORMATION SYSTEMS",
    "INSURANCE AND RISK MANAGEMENT",
    "INTEGRATED TECHNOLOGY",
    "INTEGRATED TECHNOLOGY IT",
    "INTERGOVERNMENT RELATION",
    "INTERNAL AUDIT",
    "International High",
    "International High School",
    "JJAEP (Juvenile Justice Educ Pro",
    "JOHNSTON",
    "Jordan Elementary",
    "JOSLIN ELEMENTARY",
    "Joslin Elementary",
    "Kealing Middle",
    "Kealing MS",
    "Kiker Elementary",
    "Kiker Elementary School 2",
    "Kocurek Elementary",
    "Lamar Middle",
    "Lamar MS",
    "Langford Elementary",
    "LASA High",
    "LBJ Early College HS",
    "LBJ High",
    "Leadership Academy",
    "LEADERSHIP ACADEMY ALTERNATIVE CAMPUS",
    "Lee Elementary",
    "LEGAL SERVICES",
    "Liberal Arts/Science Academy (LASA)",
    "LIBRARY MEDIA CENTER",
    "Linder Elementary",
    "LITERACY",
    "Lively Middle",
    "LUCY READ PRE-K CENTER",
    "MAIL ROOM",
    "Mainspring Schools",
    "MANAGEMENT INFO SYSTEM",
    "Maplewood Elementary",
    "Martin Middle",
    "Martin MS",
    "MATH",
    "MATHEMATICS DEPT",
    "Mathews Elementary",
    "McBee Elementary",
    "McCallum High",
    "McCallum HS",
    "Media Relations",
    "MEDICAID",
    "Menchaca Elementary",
    "Mendez Middle",
    "Mendez MS",
    "Metz Elementary",
    "Metz Free",
    "Mills Elementary",
    "MIS",
    "MULTILINGUAL EDUCATION",
    "Murchison Middle",
    "Murchison MS",
    "Murchison MS 2",
    "Navarro Early College HS",
    "Navarro High",
    "NELSON FIELD/UTILITY BUDGET",
    "NETWORK SUPPORT SRVCS",
    "Noack Sports Complex",
    "Norman-Sims Elementary",
    "Northeast Early College HS",
    "Northeast High",
    "O. Henry Middle",
    "O. Henry MS",
    "Oak Hill Elementary",
    "Oak Springs Elementary",
    "Odom Elementary",
    "Odom Elementary School 2",
    "OFF OF SCHOOL LEADERSHIP",
    "OFFICE OF EQUITY",
    "OFFICE OF INNOV & DEVELOPMENT",
    "OFFICE OF PLANNING & ASSETS",
    "OFFICE OF PROGRAM EVALUATION",
    "OPERATIONS",
    "Ortega Elementary",
    "Overton Elementary",
    "Padron Elementary",
    "Palm Elementary",
    "Paredes Middle",
    "Paredes MS",
    "Patton Elementary",
    "PEARCE MIDDLE",
    "Pease Elementary",
    "Pecan Springs Elementary",
    "Perez Elementary",
    "PERFORMING ARTS",
    "PERFORMING ARTS CENTER",
    "Phoenix Academy",
    "PHYSICAL EDUCATION",
    "Physical Education",
    "Pickle Elementary",
    "Pillow Elementary",
    "PLANT IMPROVEMENTS",
    "PLEASANT HILL ANNEX",
    "Pleasant Hill Elementary",
    "PRIME TIME",
    "PRINT SHOP",
    "Professional Development Center",
    "Program Evaluation",
    "PURCHASING",
    "Reilly Elementary",
    "Richards Sch Young Women Leaders",
    "Ridgetop Elementary",
    "Rodriguez Elementary",
    "Rosedale",
    "Sadler Means YWLA",
    "Sadler Means YWLA",
    "SAEGERT TRANS CENTER/UTIL BDGT",
    "Sanchez Elementary",
    "Sarah Lively MS",
    "SCHOOL FAMILY & COMMUNITY ED",
    "SCIENCE DEPT",
    "SCIENCE/HEALTH RES CTR",
    "SERVICE CENTER BLDG & GROUNDS",
    "SERVICE CENTER FOR VEHICLES",
    "SERVICE CENTER HOUSEKEEPING",
    "SETON HEALTH SERVICES",
    "SFCE - Southfield Building",
    "Sims Elementary",
    "Sims Elementary School",
    "Small Middle",
    "Small MS",
    "SOCIAL AND EMOTIONAL LEARNING DEPT",
    "SOCIAL EMOTIONAL LEARNING",
    "Social Studies Dept",
    "SOUTH BUS TERMINAL",
    "SPECIAL ED EVAL SERVICES",
    "SPECIAL EDUCATION",
    "SPECIAL EDUCATION AH/VH",
    "Special Education AI Dept.",
    "Special Education AT Dept.",
    "Special Education Primary",
    "Special Education VI Dept.",
    "St Elmo Elementary",
    "STATE DEAF",
    "STATE/FED CMPLNCE & ACCNTBLTY",
    "STEM",
    "STUDENT SERVICES",
    "Student Teachers",
    "SUBSTITUTE",
    "Summer Schl 411",
    "Summer Schl 421",
    "Summer Schl 446",
    "Summer Schl 457",
    "Summer Schl 459",
    "Summer Schl 463",
    "Summitt Elementary",
    "Sunset Valley Elementary",
    "SUPERINTENDENT",
    "Superintendent",
    "SYSTEM WIDE TESTING",
    "TALENT ACQUISITION & DEVELOPMENT",
    "TDT - Howard Martin",
    "Tech Paid Main",
    "Technology Main",
    "Technology Paid",
    "Test",
    "TEXAS FUTURE PROBLEM SOLVING",
    "Texas Literacy (English)",
    "Transportation Dept",
    "TRANSPORTATION OFFICE",
    "Travis County Day School",
    "Travis County Juvenile Deten Ctr",
    "Travis Early College HS",
    "Travis Heights Elementary",
    "Travis High",
    "Uphaus Early Childhood Ctr",
    "VISUAL ARTS",
    "Walnut Creek Elementary",
    "Warranty Replaced Devices",
    "Webb Middle",
    "Webb MS",
    "Webb Primary Center",
    "Widen Elementary",
    "Williams Elementary",
    "Winn Elementary",
    "Wooldridge Elementary",
    "Wooten Elementary",
    "WORLD LANGUAGE",
    "Zavala Elementary",
    "Zilker Elementary",
]