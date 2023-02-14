import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import sys
import time


import get_data
import click_functions
import parse_inputs
import unzip_and_parse


# this code checks to see if a valid file with a list of UnitIDs was given as input
# if not, it will use the default list of Big Ten Schools as input
# also check for if a list of years is given in a text file
inputs = parse_inputs.parse_inputs(sys.argv)
years = inputs[0]
unitIDs = inputs[1]

if unitIDs == "":
    print("List of UnitIDs not given, using default of Big10 Schools.")
    unitIDs = "145637, 153658, 174066, 181464, 147767, 243780, 240444, 151351, 163286, 170976, 171100, 204796, 214777, 186380, 144050"
if years == []:
    print("List of years not given, will search latest year")

# temporarily installs correct chromedriver needed for selenium 
chromedriver_autoinstaller.install()
# defines driver variable for use throughout
driver = webdriver.Chrome()
# opens chrome to the following url
driver.get('https://nces.ed.gov/ipeds/datacenter/default.aspx?gotoReportId=5&fromIpeds=true')

# find textbox for searching for institution
inst_tb = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tbInstitutionSearch"]')))
# enter test_UnitID into textbox
driver.execute_script("arguments[0].setAttribute('value',arguments[1])",inst_tb, unitIDs)
# click "select" button to search for UnitID
driver.find_element(By.ID, 'contentPlaceHolder_ibtnSelectInstitutions').click()

# waits until continue button has loaded in
continue_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="contentPlaceHolder_ibtnContinue"]')))

# clicks Check All link
driver.find_element(By.XPATH, '//span[text()="Check All"]').click()

# find all checkboxes that have been loaded and click them
# check_boxes = driver.find_elements(By.ID, 'cbUnitId')
# for check_box in check_boxes:
#     check_box.click()

# click continue button
continue_btn.click()

view_data_continue_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="contentPlaceHolder_divInstructions"]/table/tbody/tr/td[2]/a/img'))).click()

## finding data matching table as shown here: https://btaa-sitefinity.azurewebsites.net/docs/default-source/research-data/at-a-glance-2019-ipeds-with-2020-rankings-btaa.pdf?sfvrsn=393cfc1b_2
# getting data based on what years are wanted by user

# if no year file given, just get data from 2020
if len(years) == 0:
    avail_years = driver.find_elements(By.XPATH, "//a[contains(text(), '2020')]")
    avail_years[0].click()
    get_data.get_data(2020, driver) # 2020 not necessary, just has to be at least 2019
# if year file give, get data from all the years in file
else:
    for year in years:
        year = year.rstrip()
        click_functions.click_something("//a[contains(text(), '" + year + "')]", driver)
        time.sleep(1)
        get_data.get_data(int(year), driver)
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.HOME)
        time.sleep(1)

# click continue
click_functions.click_something('//*[@id="imgContinueButton"]', driver)
# find all CSV links that contain all the data for a particular year
csv_links = driver.find_elements(By.XPATH, '//a[contains(@href,"singleFile=true&command=csv")]')

# click each year's full data link
for csv_link in csv_links:
    csv_link.click()

time.sleep(5)

driver.quit()

unzip_and_parse.get_all_data(len(csv_links))