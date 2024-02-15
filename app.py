
from utils.helpers import *

# Constants
LIMIT = 20 # number of responses until which random activity will be done to keep the session active
URL ='https://cibnext.icicibank.com/corp/AuthenticationController?FORMSGROUP_ID__=AuthenticationFG&__START_TRAN_FLAG__=Y&FG_BUTTONS__=LOAD&ACTION.LOAD=Y&AuthenticationFG.LOGIN_FLAG=1&BANK_ID=ICI'
Logs_status = True # Change it to 'False' if you don't want logs to be saved

# Credential import from credentials.txt (one line comma separated username and password)
with open('credentials.txt') as f:
    lines = f.read().split(',')
    username = lines[0]
    password = lines[1]

# Login to URL
driver = login(username, password,URL)

# Get the shadow root for chatbox
shadow_root = initialize_chatbot(driver)

# get the list of prompts from csv
df = pd.read_csv('prompt.csv')

# Batch prompt the list of prompts
batch_prompt(driver,shadow_root,df,LIMIT,Logs_status)

# Final actual save
clean_and_save(df,'reverse.csv')
print('Final data saved to reverse.csv')






