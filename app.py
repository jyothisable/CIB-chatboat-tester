
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import chromedriver_binary
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains 
import os.path
from datetime import datetime

# Constants
LIMIT = 20 # number of responses until which random activity will be done to keep the session active
URL ='https://cibnext.icicibank.com/corp/AuthenticationController?FORMSGROUP_ID__=AuthenticationFG&__START_TRAN_FLAG__=Y&FG_BUTTONS__=LOAD&ACTION.LOAD=Y&AuthenticationFG.LOGIN_FLAG=1&BANK_ID=ICI'

# Import driver
driver = webdriver.Chrome()

# Open the login page
driver.get(URL)
# Wait for the page to load completely
time.sleep(2)

# Credential import from credentials.txt (one line comma separated username and password)
with open('credentials.txt') as f:
    lines = f.read().split(',')
    username = lines[0]
    password = lines[1]

def login(username, password):
    '''
    Complete login and go to home page
    '''
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
    
    print('Login Successful')


login(username, password)

def initialize_chatbot():
    '''
    Initiate chatbot and give the shadow root (like 2nd fake root for only this widget)
    '''
    # Find chatbot button
    shadow_root = driver.find_element(By.CSS_SELECTOR, '#shadow').shadow_root

    shadow_root.find_element(By.CSS_SELECTOR,'div.wrapper-container > button').click()
    time.sleep(2)
    print('Chatbot initialized successfully')
    return shadow_root
    
shadow_root = initialize_chatbot()

def get_response(prompt):
    '''
    For a given prompt gives all the response with '#' as seperator
    '''
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

def do_some_random_activity():
    '''
    Minimize the chatbot then move the cursor down and up to keep the session active then open the chatbox again
    '''
    # click on minimize
    shadow_root.find_element(By.CSS_SELECTOR, '#minimize').click()
    
    # Other activity click
    # Create an ActionChains object
    actions = ActionChains(driver)

    # Scroll down and up by  100 pixels
    actions.move_to_element(driver.find_element(By.XPATH,'//*[@id="GroupletPanel.SubSection2"]/div[3]/div[1]'))
    actions.click()
    actions.send_keys(Keys.PAGE_DOWN)
    actions.send_keys(Keys.PAGE_UP)

    # Perform the action
    actions.perform()
    
    # click on chat button 
    shadow_root.find_element(By.CSS_SELECTOR,'div.wrapper-container > button').click()
    time.sleep(2)
    
    print('Session timeout extended successfully')

# get the list of prompts from csv
df = pd.read_csv('prompt.csv')

def batch_prompt():
    print('Initiating Prompt Engine')
    
    df['Response'] = None
    # Split the prompts to limit columns such that response can be saved to csv file in between
    for i in range(len(df)):
        df['Response'].iloc[i] = get_response(df['Prompts'].iloc[i])
        if i%LIMIT == 0:
            df_limit =pd.concat([df['Prompts'],df['Response'].str.split(pat='#',regex=False , expand=True)], axis=1)

            # timestamped log file
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'logs/reverse_{timestamp}.csv'

            # Save the DataFrame to the CSV file
            df_limit.iloc[:i+1].to_csv(filename, index=False)

            print(f"{i%LIMIT+1}th batch completed. Data saved to {filename}")
            
            do_some_random_activity()

batch_prompt()

# Final actual save
df_final = pd.concat([df['Prompts'],df['Response'].str.split(pat='#',regex=False , expand=True)], axis=1)
df_final.to_csv('reverse.csv', index=False,mode='w')
print('Final data saved to reverse.csv')






