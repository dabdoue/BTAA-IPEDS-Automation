from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver

def click_something(xpath, driver):
    
    try:
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
    except KeyboardInterrupt:
        quit()
    except:
        last_height = driver.execute_script("return document.body.scrollHeight")
        cur_height = driver.execute_script("return window.scrollY")
        if last_height > cur_height + 300:
            driver.execute_script("window.scrollTo(0, window.scrollY + 300)")
            print("could not find element:" + xpath)
            click_something(xpath, driver)
        else:
            quit()

def click_dropdown(value, driver):
    xpath = "//div[contains(text(), '" + value + "')]"
    click_something(xpath, driver)

def click_checkbox(value, driver):
    xpath = "//label[contains(text(), '" + value + "')]"
    click_something(xpath, driver)