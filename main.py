
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import chromedriver_binary
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains 

driver = webdriver.Chrome()

# Open the login page
driver.get('https://cibnext.icicibank.com/corp/AuthenticationController?FORMSGROUP_ID__=AuthenticationFG&__START_TRAN_FLAG__=Y&FG_BUTTONS__=LOAD&ACTION.LOAD=Y&AuthenticationFG.LOGIN_FLAG=1&BANK_ID=ICI')

# Wait for the page to load completely
time.sleep(2)

# Credential import from credentials.txt
with open('credentials.txt') as f:
    lines = f.read().split(',')
    username = lines[0]
    password = lines[1]


# Find the username field and enter the username
username_field = driver.find_element(By.XPATH,'/html/body/form[1]/div[3]/main/div/div[1]/div[1]/div/div[2]/div[1]/div/div/input')
username_field.clear()
username_field.send_keys(username)


# Find the password field and enter the password
password_field = driver.find_element(By.XPATH,'//*[@id="AuthenticationFG.ACCESS_CODE"]')
password_field.send_keys(password)

time.sleep(3)

# find submit button
driver.find_element(By.XPATH,'//*[@id="LoginHDisplay"]/main/div/div[1]/div[1]/div/div[2]/div[8]').click()

time.sleep(5)



