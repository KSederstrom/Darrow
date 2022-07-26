import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd
import xlwings as xw
from getpass import getuser
from bs4 import BeautifulSoup
import random

# class creation
class Morningstar_bot():

    # instantiate class
    def __init__(self, ticker):

        # class attributes and functionality
        url_MS = f'https://www.morningstar.com/funds/xnas/{ticker}/quote'
        url_TD = f'https://research.tdameritrade.com/grid/public/mutualfunds/profile/performanceBuffer.asp?symbol={ticker}'

        self.ticker = ticker
        #establish google chrome as the default webbrowser to use when calling driver
        self.driver = webdriver.Chrome(r'C:\Users\1263654\Desktop\chromedriver.exe')
        #self.driver = webdriver.Edge(r'C:\Users\1263654\Desktop\msedgedriver.exe')

        """  Important: These are the xpath references to the desired metrics.
        These may change some day. Be sure to update if any errors arise. It will flow through the rest of the process.
        If xpath references (self.r_square for example) go to the website and find the section that we are wanting to grab or click.  Right click and 
        inspect or inspect HTML. Highlight over the code in the window on the right that appeared. Should highlight respective area on the webpage.
        Find the ones that are span, usually. Right click on that line, copy, copy Xpath. Do not do full Xpath, that is different.
        Step 1: Enter the ticker symbol within the search box (top left of sheet, A1). Do not have any blanks in the column otherwise it may error."""

        # paths to metrics
        self.NE ='//*[@id="__layout"]/div/div/div[2]/div[3]/div/main/div[2]/div/div/div/section[1]/div[1]/div[4]/div[2]/span/span'
        self.Risk_tab = '//*[@id="fund__tab-risk"]/a/span/span'

        #Go to morningstar page, sleep for 2 seconds while it loads, grab NE, and then go to the risk page and sleep for 2 seconds while it loads
        self.driver.get(url_MS)
        sleep(5) # wait for 2 seconds
        net_expense = self.driver.find_element_by_xpath(self.NE).get_attribute('innerHTML') # Span is the path with the actual value
        self.driver.find_element_by_xpath(self.Risk_tab).click()
        sleep(3) # wait for 2 seconds

        # paths to metrics on Risk page.   - Span is the path with the actual value
       # self.r_square = '//*[@id="__layout"]/div/div/div[2]/div[3]/div/main/div[2]/div/div/div/sal-components/div/sal-components-funds-risk/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]/table/tbody/tr[3]/td[2]/span'
                         
        self.r_square = '//*[@id="__layout"]/div/div/div[2]/div[3]/div/main/div[2]/div/div/div[1]/sal-components/div/sal-components-funds-risk/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]/table/tbody/tr[3]/td[2]/span'
        self.sharpe_ratio = '//*[@id="__layout"]/div/div/div[2]/div[3]/div/main/div[2]/div/div/div[1]/sal-components/div/sal-components-funds-risk/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]/table/tbody/tr[4]/td[2]/span'
        self.stdev = '//*[@id="__layout"]/div/div/div[2]/div[3]/div/main/div[2]/div/div/div[1]/sal-components/div/sal-components-funds-risk/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]/table/tbody/tr[5]/td[2]/span'
        self.MS_date = '//*[@id="__layout"]/div/div/div[2]/div[3]/div/main/div[2]/div/div/div[1]/sal-components/div/sal-components-funds-risk/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div[2]/span[2]/span[3]'


        # Now that you are on Risk page, grab Rsquare, the sharpe, and the standard deviation values for three years. 
        r2_3 = self.driver.find_element_by_xpath(self.r_square).get_attribute('innerHTML') 
        sharpe_3 = self.driver.find_element_by_xpath(self.sharpe_ratio).get_attribute('innerHTML')
        stdev_3 = self.driver.find_element_by_xpath(self.stdev).get_attribute('innerHTML')
        MS_data_date = self.driver.find_element_by_xpath(self.MS_date).get_attribute('innerHTML')

        # Navigate to 5 year section of Risk and pull info.
        #self.driver.find_element_by_xpath('//*[@id="'+id_tag+'"]/div/mds-button-group/div/slot/div/mds-button[2]/label/input').click() 
        self.driver.find_element_by_xpath('//*[@id="for5Year"]').click()
        sleep(3)
        r2_5 = self.driver.find_element_by_xpath(self.r_square).get_attribute('innerHTML')
        sharpe_5 = self.driver.find_element_by_xpath(self.sharpe_ratio).get_attribute('innerHTML')
        stdev_5 = self.driver.find_element_by_xpath(self.stdev).get_attribute('innerHTML')

        # 10 year Risk metrics
        #self.driver.find_element_by_xpath('//*[@id="'+id_tag+'"]/div/mds-button-group/div/slot/div/mds-button[3]/label/input').click()
        self.driver.find_element_by_xpath('//*[@id="for10Year"]').click()
        sleep(2)
        r2_10 = self.driver.find_element_by_xpath(self.r_square).get_attribute('innerHTML')
        sharpe_10 = self.driver.find_element_by_xpath(self.sharpe_ratio).get_attribute('innerHTML')
        stdev_10 = self.driver.find_element_by_xpath(self.stdev).get_attribute('innerHTML')

        #Go to TDAmeritrade page, sleep for 2 seconds while it loads, grab 3 5 and 10 yr return and the date.
        self.driver.get(url_TD)
        sleep(4)

        return_3 = self.driver.find_element_by_xpath('//*[@id="table-trailingTotalReturnsTable"]/tbody/tr[5]/td[2]').get_attribute('innerHTML')
        return_5 = self.driver.find_element_by_xpath('//*[@id="table-trailingTotalReturnsTable"]/tbody/tr[6]/td[2]').get_attribute('innerHTML')
        return_10 = self.driver.find_element_by_xpath('//*[@id="table-trailingTotalReturnsTable"]/tbody/tr[7]/td[2]').get_attribute('innerHTML')

       # remove blank spaces from return numbers and clean up dirty sections from others.
        return_3 = ''.join(return_3.split('<span class="positive">'))
        return_3 = ''.join(return_3.split('%</span>'))
        return_5 = ''.join(return_5.split('<span class="positive">'))
        return_5 = ''.join(return_5.split('%</span>'))
        return_10 = ''.join(return_10.split('<span class="positive">'))
        return_10 = ''.join(return_10.split('%</span>'))

        # create metric dictionary
        self.metric_dict = {
            'Morningstar Date': MS_data_date,
            'Net Expense Ratio': net_expense,
            '3 Year Rsquare': r2_3,
            '3 Year Sharpe Ratio': sharpe_3,
            '3 Year Standard Deviation': stdev_3,
            '3 year return': return_3,

            # 5 year
            '5 Year Rsquare': r2_5,
            '5 Year Sharpe Ratio': sharpe_5,
            '5 Year Standard Deviation': stdev_5,
            '5 Year Return': return_5,
            # 'S&P 5 Year Return': SnP_return_5,
        
            # 10 year
            '10 Year Rsquare': r2_10,
            '10 Year Sharpe Ratio': sharpe_10,
            '10 Year Standard Deviation': stdev_10,
            '10 Year Return': return_10
            # 'S&P 10 Year Return': SnP_return_10
        }

def fund_scrape(excel_path, csv_outputpath):

    """ 
    Calls the morningstar scrape bot and reads in tickers from excel sheet.
   It references the default sheet name, and uses column A to extract tickers. 
   """

    try:
        # Import list from Excel Template
        excel_doc = xw.Book(f'{excel_path}')
        sheet = excel_doc.sheets['Sheet1']

        # extract ticker list (from column A) as list. Selet if running first half or second half here:
        #tickers = sheet.range('A:A').value
        #tickers = sheet.range('B:B').value
        tickers = sheet.range('C:C').value
        #tickers = sheet.range('D:D').value
        #tickers = sheet.range('E:E').value
        tickers = [tick for tick in tickers if tick if tick != 'Ticker'] # if tick removes None values
#vrivx unlocatable.

        """
        Loop through list of funds within the Excel spreadsheet
        """
        metrics_list = []
        # testing update
        for i in tickers:
            print(i)
            # i=tickers[0] #This has to be delted
            metrics_list.append(Morningstar_bot(ticker=i).metric_dict)

        # create dictionary
        ticker_dict = dict(zip(tickers[0:250], metrics_list))
        ticker_df = pd.DataFrame.from_dict(ticker_dict)
        #ticker_df.to_csv(csv_outputpath + '\\Fund_metrics_MSandTD_part1.csv')
        #ticker_df.to_csv(csv_outputpath + '\\Fund_metrics_MSandTD_part2.csv')
        ticker_df.to_csv(csv_outputpath + '\\Fund_metrics_MSandTD_part3.csv')
        #ticker_df.to_csv(csv_outputpath + '\\Fund_metrics_MSandTD_part4.csv')
        #ticker_df.to_csv(csv_outputpath + '\\Fund_metrics_MSandTD_part5.csv')
        # success
        print('The file was exported to the csv_outputpath as Fund_metrics_MSandTD.csv')

    except:
        print('The scrape did not run successfully')

fund_scrape(excel_path=r'F:\401K\1. 401K & ESOP\User - Karsten\401k-ESOP-Canada\Fund Performance Review\Ticker_trials.xlsx', csv_outputpath=r'C:\Users\1263654\Desktop')



