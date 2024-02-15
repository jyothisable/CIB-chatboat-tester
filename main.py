
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

# set session timeout widget z-index to 1
session_timeout_widget = driver.find_element(By.CSS_SELECTOR, "overlaySessionAlert")
driver.execute_script("arguments[0].style.zIndex = '1'", session_timeout_widget)

# Find chatbot button
shadow_root = driver.find_element(By.CSS_SELECTOR, '#shadow').shadow_root

shadow_root.find_element(By.CSS_SELECTOR,'div.wrapper-container > button').click()
time.sleep(2)

def get_response(prompt):
    # Find input prompt field
    input_field = shadow_root.find_element(By.CSS_SELECTOR, 'div.chat-window > div.chat-footer > input')
    input_field.send_keys(prompt)

    time.sleep(1)

    # Find send button
    shadow_root.find_element(By.CSS_SELECTOR, 'div.chat-window > div.chat-footer > img.chat-send-button').click()
    time.sleep(5)

    # Find the response
    responses = shadow_root.find_elements(By.CSS_SELECTOR, 'div.chat-window > div.chat-messages > div > div:last-child > *')
    res_string = ''
    for idx in range(len(responses)-1):
        res_string += str(responses[idx].text) + '#'
    return res_string

# get the list of prompts from csv
df = pd.read_csv('prompt.csv')
df['Response'] = df['Prompts'].map(lambda x: get_response(x))


df2 = pd.concat([df['Prompts'], df['Response'].str.split('#', expand=True)], axis=1)

print(df2)
df2.to_csv('reverse.csv')




