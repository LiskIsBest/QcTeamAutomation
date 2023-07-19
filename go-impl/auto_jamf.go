package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"syscall"
	"strings"
	"runtime"

	"github.com/go-rod/rod"
	"golang.org/x/crypto/ssh/terminal"
)

const JAMF_URL string = "https://login.jamfschool.com/login"
const JAMF_DEVICES_URL string = "https://austinisd.jamfcloud.com/devices"
const FORCE_MOVE_JAVASCRIPT string = "document.getElementById(\"force-move-option-checkbox\").click()"
const JAMF_EMAIL string ="#email"
const JAMF_PASSWORD string ="#password"
const JAMF_SIGN_IN_BUTTON string ="button[type=\"submit\"]"
const JAMF_SIGN_IN_ERROR string =".error-text__29lYK"
const JAMF_AUTH_FORM string ="//*[@id=\"app\"]/div/div/article/div/form/div[1]/div[2]/input"
const DEVICES_SIDE_MENU string ="//*[@id=\"app\"]/aside/nav[1]/ul/li[2]/a"
const DEVICES_SIDE_MENU2 string = "a[data-target=\"#devices\"]"
const INVENTORY_SEARCH string = "input[placeholder=\"Search...\"]"
const FIRST_IPAD_RESULT string = "//*[@id=\"app\"]/main/div/div[2]/div/div/table/tbody/tr/td[2]/div/div[2]/a"
const EDIT_DETAILS_BUTTON string = "//*[@id=\"details\"]/div/div[1]/div/a"
const USER_BOX string = "//*[@id=\"owner-id\"]/option"
const CURRENT_USER string = "select2-selection__clear"
const ERASE_IPAD_BUTTON string = "//*[@id=\"importantButton\"]"
const ERASE_IPAD_CONFIRM string = "#wipe-submit"
const LOCATION_CHANGE_BUTTON string = "toggle-move-to-location"
const SCHOOL_LIST_DROP_DOWN string = "#select-new-location"
const SAVE_DETAILS_BUTTON string = "modal-move-to-location-submit"
const SAVE_IPAD_BUTTON string = "#btn-edit"

// ANSI escape characters for colors
// Border color "Yellow"
const BC string = "\033[0;33m"
// Title color "Cyan"
const TC string = "\033[0;36m"
// Warning color "Red"
const WC string = "\033[0;31m"
// Color terminator
const CT string = "\033[00m"

func main(){
	read_in := bufio.NewReader(os.Stdin)
	
	fmt.Print("Enter the location name (check jamf for exact name): ")
	school, err := read_in.ReadString('\n')
	if err != nil{
		log.Fatalln(err)
	}
	school = strings.TrimSuffix(school, "\n")

	fmt.Print("Enter Jamf username/email: ")
	email, err := read_in.ReadString('\n')	
	if err != nil{
		log.Fatalln(err)
	}
	email = strings.TrimSuffix(email,"\n")

	var password string
	switch os:=runtime.GOOS; os{
	case "linux":
		fmt.Print("Enter your Jamf password: ")
		ipassword, err := terminal.ReadPassword(0)
		if err != nil{
			log.Fatalln(err)
		}
		fmt.Println()
		password = string(ipassword)
	case "windows":
		ipassword, err := terminal.ReadPassword(int(syscall.Stdin))
		if err != nil{
			log.Fatalln(err)
		}
		fmt.Println()
		password = string(ipassword)
	}
	password = strings.TrimSuffix(password, "\n")

	driver := rod.New().MustConnect().MustPage(JAMF_URL)
	jamf_login(driver, email, password)

	for {
		fmt.Print("Scan serial number or asset tag (0 to quit): ")
		SNorASSET, err := read_in.ReadString('\n')
		if err != nil {
			log.Fatalln(err)
		}
		SNorASSET = strings.TrimSuffix(SNorASSET, "\n")
		if SNorASSET == "0"{
			break
		}
		fmt.Println(SNorASSET)
	}
}

func jamf_login(driver *rod.Page, email string, password string){
	driver.MustElement(JAMF_EMAIL).MustInput(email)
	driver.MustElement(JAMF_PASSWORD).MustInput(password)
	driver.MustElement(JAMF_SIGN_IN_BUTTON).MustClick()
	driver.MustElement(DEVICES_SIDE_MENU2)
	driver.MustNavigate(JAMF_DEVICES_URL)
	driver.MustElement(INVENTORY_SEARCH)
}

func jamf_ipad(driver *rod.Page, SNorASSET string, school string){

}