from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import urllib, time, random, json, pandas as pd, numpy as np
from datetime import date
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import simpledialog

import regex

psw_url = 'https://sponsor.fidelity.com/pspublic/pca/psw/public/homepage.html'
psw_reports_URL = 'https://plansponsorservices.fidelity.com/plansponsor/intreporting/showRunReports.psw'

ROOT = tk.Tk()
ROOT.withdraw()
# the input dialog
#username = simpledialog.askstring(title="PSW Login ingo",
#                                  prompt="PSW username:")
password = simpledialog.askstring(title="Security Code",
                                  prompt="PSW password:")

#Hardcoding Username and password
username = 'WPH724E'

#establish google chrome as the default webbrowser to use when calling driver
chrome_options = Options()
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("--incognito")a
#driver = webdriver.Chrome(r'C:\Users\1263654\Desktop\chromedriver.exe', options=chrome_options)
driver = webdriver.Edge(r'C:\Users\1263654\Desktop\msedgedriver.exe')

driver.get(psw_url)
# find username/email field and send the username itself to the input field
driver.find_element_by_id("userid").send_keys(username)

# find password input field and insert password as well
driver.find_element_by_id("pin").send_keys(password)
# click login button
driver.find_element_by_id("fs-login-button").click()
WebDriverWait(driver=driver, timeout=2)
time.sleep(1)
#Selects phone number option (click)
driver.find_element_by_id("phone-label-0").click()
driver.find_element_by_xpath('//*[@id="step-challenge"]/form/div[2]/div').click()
WebDriverWait(driver=driver, timeout=2)
time.sleep(1)
#selects text to the phone number option (click)
driver.find_element_by_id("channel-label-sms").click()
driver.find_element_by_xpath('//*[@id="step-selectChannel"]/form/div/div[3]/div/div[2]/button').click()
WebDriverWait(driver=driver, timeout=2)
time.sleep(1)

#Input Security Code
ROOT = tk.Tk()
ROOT.withdraw()
# the input dialog
securitycode = simpledialog.askstring(title="Security Code",
                                  prompt="Enter the Fidelity Code:")

driver.find_element_by_id("code").send_keys(securitycode)
driver.find_element_by_xpath('//*[@id="validateCodeForm"]/div[4]/div/div/button').click()


time.sleep(2)

#Go to the PSW reports page.
driver.get(psw_reports_URL)
psw_reports_URL = 'https://plansponsorservices.fidelity.com/plansponsor/intreporting/showRunReports.psw'


#Input Report name
ROOT = tk.Tk()
ROOT.withdraw()
## the input dialog
#reportname = simpledialog.askstring(title="Report",
#                                  prompt="Enter the PSW Report name, specific please:")
reportname = 'audit deferral change'

driver.find_element_by_id("keyword-search").send_keys(reportname)
#Search Bar
driver.find_element_by_xpath('//*[@id="keyword-search"]').click()
#Button for filter table
driver.find_element_by_xpath('//*[@id="buttonWrap"]/a[2]').click()
#Click on the first report in the list.
driver.find_element_by_xpath('//*[@id="dojox_grid__View_1"]/div/div/div/div/table/tbody/tr[1]/td[1]/form/a').click()



#Plan Number: 75951;75952        //*[@id="saw_135679734_2_1"] Numbers for xpath will change.   //*[@id="saw_135687597_4_1"]
#Date start: 01/01/2019 12:00:00 AM              //*[@id="saw_135679734_3_1_D"]   - -//*[@id="saw_135687597_5_1_D"]

#Date end: 12/31/2020 12:00:00 AM               //*[@id="saw_135679734_3_2_D"]        //*[@id="saw_135687597_5_2_D"]

url_soup = BeautifulSoup(driver.page_source, "html.parser")
stringname = str (url_soup) 

python regex find string. 
Name_id_tag = str(test_Name_id_tag.find_all("input")[1]).split('" ')[1]

net_expense = ''.join(net_expense.split('<span class="mdc-data-point mdc-data-point--number" data-v-7ba8d775="" data-v-8645dbb6="">'))
