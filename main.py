
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import chromedriver_binary
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains 
import os.path
from datetime import datetime


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

df['Response'] = None

# Split the prompts to limit columns such that response can be saved to csv file in between
limit = 2
for i in range(len(df)):
    df['Response'].iloc[i] = get_response(df['Prompts'].iloc[i])
    if i%limit == 0:
        df_limit =df['Response'].str.split('#', expand=True)

        # timestamped log file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'logs/reverse_{timestamp}.csv'

        # Save the DataFrame to the CSV file
        df.iloc[:i+1].to_csv(filename, index=False)

        print(f"Data saved to {filename}")
        
        # do activity to extend the session timeout
        # click on minimize
        shadow_root.find_element(By.CSS_SELECTOR, '#minimize').click()
        
        # Other activity click
        # Create an ActionChains object
        actions = ActionChains(driver)

        # Scroll down by  100 pixels
        actions.move_to_element(driver.find_element(By.XPATH,'//*[@id="GroupletPanel.SubSection2"]/div[3]/div[1]'))
        actions.click()
        actions.send_keys(Keys.PAGE_DOWN)
        actions.send_keys(Keys.PAGE_UP)

        # Perform the action
        actions.perform()
        
        # click on chat button 
        shadow_root.find_element(By.CSS_SELECTOR,'div.wrapper-container > button').click()
        time.sleep(2)
        
while os.path.exists(filename):
    # Append a timestamp to the filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'my_data_{timestamp}.csv'

# Final actual save
df.to_csv('reverse.csv', index=False)






