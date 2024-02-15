# Chatbot automation testing using selenium for a Corporate Internet Banking website
This is my first project using selenium for automation of website testing

This script is configured to run on ICICI Bank CIB website.

Please note that this may not properly working in future if XPath or CSS selector gets changed.

## Features
Using this python application you can test any number of prompts using a csv file as input. A reverse file will be generated will corresponding responses (single / multiple) mapped along the same records.

Session timeout is extended by random auto clicks

## Getting started
### Prerequisites
List of software and packages required to install and run the project.
* Python 3.x
* Selenium WebDriver
* Chrome Browser
* Chromedriver Binary
* Anaconda - optional


### Installation and usage
1. Install anaconda 
2. Replicate the environment using `/environment.yml` file
3. Clone the repository
4. Input all the prompts to be tested in `/Prompts.csv` file under `Prompts` header
5. Run the script from `/app.py`
6. Output will be available in the `/Response_timestamp.csv` file

#### Configurable Params
1. `Logs_status = True / False` : To enable / disable data logging the results in between to avoid loss of data
2. `LIMIT = 20` : This defines the number of prompts after which some random activity will be done to keep the session active 

## Authors
Athul Jyothis  - @jyothisable

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.

## Acknowledgments
This was a late night one day project I did for testing couple of (I mean a huge list of) prompts I wanted to test and see if AI powered chatbot in the internet banking website is working properly or not.

Feel free to fork and reach out for support if needed.

Please note that this may not properly working in future if XPath or CSS selector gets changed.