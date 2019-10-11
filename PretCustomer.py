from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import time
import random 
import string 
import subprocess 

TEST_URL = "https://www.fadvisor.net/blog/"

# generating random strings of min/max 4/10 charracters for first and last name
first_name = ''.join([random.choice(string.ascii_letters) for n in range(random.randint(4, 10))])
last_name  = ''.join([random.choice(string.ascii_letters) for n in range(random.randint(4, 10))])
email = first_name + last_name + "@gmail.com"


# make the driver headless 
options = Options()
options.headless = True

browser = webdriver.Firefox(options=options, service_log_path='/home/echologic/debug.log')

# request url
browser.get(TEST_URL)

# if redirected to login page
if browser.current_url != TEST_URL:
    print("Captive portal active, attempting to authenticate with ", first_name, last_name, email)
    subprocess.Popen(['notify-send', "Captive Portal Auto-login", "Attempting authentication..."])

    try:
        fname = browser.find_element_by_name("firstName")
        fname.send_keys(first_name)
        lname  = browser.find_element_by_name("LastName")
        lname.send_keys(last_name)
        mail  = browser.find_element_by_name("email")
        mail.send_keys(email)
        cbox = browser.find_element_by_xpath("/html/body/form/div/div[2]/div/table/tbody/tr/td/div/div[9]/div/label[1]")
        actions = ActionChains(browser)
        actions.move_to_element(cbox).click().perform()
        time.sleep(2)
        signInButton = browser.find_element_by_class_name("skyfii-registrationSubmit-button")
        signInButton.click()

        # wait for the alert and accept it 
        WebDriverWait(browser, 2).until(EC.alert_is_present(),
                'Waiting for insecure connection alert to appear...')
        alert = browser.switch_to_alert()
        alert.accept()

        # wait for redirect to finish
        time.sleep(3)
        #WebDriverWait(browser, 2).until(EC.url_to_be('https://www.pret.co.uk/en-gb', 
        #    'Waiting for redirection to finish...'))
    
    except Exception as e:
        print(e)

else : 
    print("Already authenticated")

# Notify user of successful authentication
subprocess.Popen(['notify-send', "Captive Portal Auto-login", "Authenticated successfully to Pret a Manger"])

# Close the browser gracefully
browser.quit()

print("Authenticated Successfully")
