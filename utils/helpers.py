
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from datetime import datetime

    
def login(username, password,URL):
    '''
    Complete login and go to home page
    '''
    # Import driver
    driver = webdriver.Chrome()
    # Open the login page
    driver.get(URL)
    # Wait for the page to load completely
    time.sleep(2)
    
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
    return driver
    
def initialize_chatbot(driver):
    '''
    Initiate chatbot and give the shadow root (like 2nd fake root for only this widget)
    '''
    # Find chatbot button
    shadow_root = driver.find_element(By.CSS_SELECTOR, '#shadow').shadow_root

    shadow_root.find_element(By.CSS_SELECTOR,'div.wrapper-container > button').click()
    time.sleep(2)
    print('Chatbot initialized successfully')
    
    return shadow_root


def get_response(shadow_root,prompt):
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

def do_some_random_activity(shadow_root,driver):
    '''
    Minimize the chatbot then move the cursor down and up to keep the session active then open the chatbox again
    '''
    # click on minimize
    shadow_root.find_element(By.CSS_SELECTOR, '#minimize').click()
    
    # Click on home page button
    driver.find_element(By.XPATH,'/html/body/form/div[3]/div[1]/div[4]/ul/li[2]/a/div/span[2]').click() # shadow_root expires on refresh
    time.sleep(5)
    # Perform the action
    actions.perform()
    
    # new shadow root created
    new_shadow_root = initialize_chatbot(driver)
    # click on chat button 
    time.sleep(2)
    
    print('Session timeout extended successfully')
    return new_shadow_root
    

def batch_prompt(driver,shadow_root,df,LIMIT,Logs_status):
    print('Initiating Prompt Engine ...')
    
    df['Response'] = None
    # Split the prompts to limit columns such that response can be saved to csv file in between
    sup = ['st','nd','rd']
    for i in range(len(df)):
        df['Response'].iloc[i] = get_response(shadow_root,df['Prompts'].iloc[i])
        if i%LIMIT == 0:
            if Logs_status== True:
                clean_and_save(df,'logs/reverse.csv') 
                n = i//LIMIT+1
                s = sup[n] if n < 4 else 'th'
                print(f"{n}{s} batch completed. Logs saved to '/logs' folder")
                
            shadow_root = do_some_random_activity(shadow_root,driver)

def clean_and_save(df,filename):
    '''
    Concats the prompts and responses and saves it to a csv file with timestamp in the name after cleaning
    '''
    df_limit =pd.concat([df['Prompts'],df['Response'].str.split(pat='#',regex=False , expand=True)], axis=1)

    # timestamped log file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = filename.split('.')[0] + f'_{timestamp}.csv'

    # Save the DataFrame to the CSV file
    df_limit.to_csv(filename, index=False)