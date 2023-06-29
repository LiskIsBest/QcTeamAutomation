import sys

from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLineEdit, QWidget, QPushButton, QLabel
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import jamfs

# bar code: C121-10623
load_dotenv()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.email = ''
        self.password = ''


        self.items_scanned = []

        # window settings
        self.setWindowTitle("Jamf auto thingy")
        self.setFixedWidth(300)
        self.setFixedHeight(200)
        
        # debug labels
        self.error_label = QLabel(text="")
        self.driver_open_label = QLabel(parent=self, text="Chrome not open")

        # email input form
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email")
        self.email_input.textChanged.connect(self.update_email)

        # password input form
        self.pass_input = QLineEdit(self)
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.textChanged.connect(self.update_password)

        #login button
        self.login_button = QPushButton(parent=self,text='Login')
        self.login_button.clicked.connect(self.login_pressed)

        # scanner item add button
        self.scanner_add_button = QPushButton(parent=self, text="Add")
        self.scanner_add_button.clicked.connect(self.scan_enter)

        # scan items clear button
        self.scanned_items_clear_button = QPushButton(parent=self, text="Clear")
        self.scanned_items_clear_button.clicked.connect(self.scan_clear)

        # scanner input form
        self.scanner_input = QLineEdit(self)
        self.scanner_input.setPlaceholderText("Scan")
        self.scanner_input.returnPressed.connect(self.scanner_add_button.click)

        # school input form
        self.school_input = QLineEdit(self)
        self.school_input.setPlaceholderText("School/Location")

        # layout section for login
        login_layout = QVBoxLayout()
        login_layout.setContentsMargins(0,0,0,0)
        login_layout.addWidget(self.email_input)
        login_layout.addWidget(self.pass_input)
        login_layout.addWidget(self.login_button)
        login_layout.addWidget(self.error_label)
        login_layout.addWidget(self.driver_open_label)

        # layout section for scanning inputs
        scanner_layout = QVBoxLayout()
        scanner_layout.addWidget(self.school_input)
        scanner_layout.addWidget(self.scanner_input)
        scanner_layout.addWidget(self.scanner_add_button)
        scanner_layout.addWidget(self.scanned_items_clear_button)

        outerLayout = QHBoxLayout()
        outerLayout.addLayout(login_layout)
        outerLayout.addLayout(scanner_layout)

        wid = QWidget()
        self.setCentralWidget(wid)
        wid.setLayout(outerLayout)

    def update_email(self, s):
        self.email = s

    def update_password(self, s):
        self.password = s

    def login_pressed(self):
        match(self.email, self.password):
            case '', '':
                self.error_label.setText('No email or password entered!')
                self.error_label.adjustSize()
                return
            case _, '':
                self.error_label.setText('No password entered!')
                self.error_label.adjustSize()
                return
            case '', _:
                self.error_label.setText('No email entered!')
                self.error_label.adjustSize()
                return
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.chrome_driver: webdriver.Chrome = webdriver.Chrome(options=chrome_options)
        self.chrome_driver.implicitly_wait(35)
        self.driver_open_label.setText('Chrome open')
        jamfs.open_jamf_site(driver=self.chrome_driver, email=self.email, password=self.password)

    def scan_enter(self):
        item = self.scanner_input.text()
        school = self.school_input.text()
        jamfs.update_jamf(driver=self.chrome_driver, SNorASSET=item, school=school)
        # self.items_scanned.append(item)
        # print(f"adding {item} to list:{self.items_scanned}")
        self.scanner_input.setText('')

    def scan_clear(self):
        self.items_scanned = []
        print(f"cleared list:{self.items_scanned}")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()