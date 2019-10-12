#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import time
import random 
import string 


TEST_URL = "https://www.fadvisor.net/blog/"

params = {
        'firstName': "",
        'LastName' : "",
        'email'    : "",
        }


# generating random strings of min/max 4/10 charracters for first and last name
def generate_random_string(min, max):
    return ''.join([random.choice(string.ascii_letters) for n in range(random.randint(min, max))])

def input_params(browser):
    for element, value in params.items():
        field = browser.find_element_by_name(element)
        field.send_keys(value)

def extra_params(browser):
     cbox = browser.find_element_by_xpath("/html/body/form/div/div[2]/div/table/tbody/tr/td/div/div[9]/div/label[1]")
     actions = ActionChains(browser)
     actions.move_to_element(cbox).click().perform()

def submit_form(browser):
    # should add to wait for the sign in button
    signInButton = browser.find_element_by_class_name("skyfii-registrationSubmit-button")
    signInButton.click()

# Checks if the captive portal is active
def is_authenticated(browser):
    try: 
        browser.get(TEST_URL)
        if browser.current_url != TEST_URL:
            return False
        else:
            return True
    except Exception as e:
        print(e)
        return False
    

# Authentication procedure
def authenticate(browser, params):
    try:
        # Input parameters into the form
        input_params(browser)
        extra_params(browser)
        
        # Waiting for the submit button
        time.sleep(2)
        submit_form(browser)
             
        # wait for the alert and accept it 
        WebDriverWait(browser, 2).until(EC.alert_is_present(),
                'Waiting for insecure connection alert to appear...')
        alert = browser.switch_to_alert()
        alert.accept()

        # wait for redirect to finish
        time.sleep(3)
    
    except Exception as e:
        print(e)


def main():
    
    # disable cache
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.cache.disk.enable", False)
    profile.set_preference("browser.cache.memory.enable", False)
    profile.set_preference("browser.cache.offline.enable", False)
    profile.set_preference("network.http.use-cache", False)
    
    # make the driver headless 
    options = Options()
    options.headless = True
    options.profile = profile

    # initialise the driver 
    browser = webdriver.Firefox(options=options, service_log_path='/home/echologic/debug.log')

    # to be change with realistic credentials from db 
    params['firstName'] = generate_random_string(4, 10)
    params['LastName'] = generate_random_string(4, 10)
    params['email'] = params['firstName'] + params['LastName'] + "@gmail.com"
    
    print("Authenticating with; ", params)
    
    # Retry clause
    authenticated = is_authenticated(browser)
    while not authenticated:
        authenticate(browser, params)
        authenticated = is_authenticated(browser)
        if authenticated:
            break
        time.sleep(1)
        print("Retryinng")

    print("Authenticated Successfully")
    
    # Close the browser gracefully
    browser.quit()

main()
