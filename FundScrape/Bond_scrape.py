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
        self.driver = webdriver.Chrome(r'C:\Users\1341951\Desktop\chromedriver.exe')
        #self.driver = webdriver.Edge(r'C:\Users\1263654\Desktop\msedgedriver.exe')

        # paths to metrics on the quote page
        self.NE = '//*[@id="__layout"]/div/div/div[2]/div[3]/div/main/div[2]/div/div/div/section[1]/div[1]/div[4]/div[2]/span/span'
        self.category = '//*[@id="__layout"]/div/div/div[2]/div[3]/div/main/div[2]/div/div/div/section[1]/div[1]/div[7]/div[2]/span'
        self.TTMyield = '//*[@id="__layout"]/div/div/div[2]/div[3]/div/main/div[2]/div/div/div/section[1]/div[1]/div[11]/div[2]/span'
        self.duration = '//*[@id="__layout"]/div/div/div[2]/div[3]/div/main/div[2]/div/div/div/section[1]/div[1]/div[12]/div[2]/span'

        #path to metrics on the risk page
        self.beta = '//*[@id="__layout"]/div/div/div[2]/div[3]/div/main/div[2]/div/div/div/sal-components/div/sal-components-funds-risk/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]/table/tbody/tr[2]/td[2]/span'
        self.r2 = '//*[@id="__layout"]/div/div/div[2]/div[3]/div/main/div[2]/div/div/div/sal-components/div/sal-components-funds-risk/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]/table/tbody/tr[3]/td[2]/span'
        self.sharpe = '//*[@id="__layout"]/div/div/div[2]/div[3]/div/main/div[2]/div/div/div/sal-components/div/sal-components-funds-risk/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]/table/tbody/tr[4]/td[2]/span'
        self.upside = '//*[@id="__layout"]/div/div/div[2]/div[3]/div/main/div[2]/div/div/div/sal-components/div/sal-components-funds-risk/div/div/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div[1]/table[1]/tbody[1]/tr[1]/td[2]'
        self.downside = '//*[@id="__layout"]/div/div/div[2]/div[3]/div/main/div[2]/div/div/div/sal-components/div/sal-components-funds-risk/div/div/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div[1]/table[1]/tbody[1]/tr[2]/td[2]'

        #Go to morningstar page, sleep for 2 seconds while it loads, grab NE, and then go to the risk page and sleep for 2 seconds while it loads
        self.driver.get(url_MS)
        sleep(5) # wait for 2 seconds
        net_expense = self.driver.find_element_by_xpath(self.NE).get_attribute('innerHTML') # Span is the path with the actual value
        category = self.driver.find_element_by_xpath(self.category).get_attribute('innerHTML') 
        TTMyield = self.driver.find_element_by_xpath(self.TTMyield).get_attribute('innerHTML') 
        duration = self.driver.find_element_by_xpath(self.duration).get_attribute('innerHTML') 



       
        #Click on the risk tab.
        #//*[@id="__layout"]/div/div[2]/div[3]/div/main/nav/ul/a[4]/span/span
        self.driver.find_element_by_xpath('//*[@id="fund__tab-risk"]/a/span/span').click()
        sleep(2) # wait for 2 seconds




        # Now that you are on Risk page, grab beta, rsquare, sharpe, the upside, and downside for three years. 
        beta_3 = self.driver.find_element_by_xpath(self.beta).get_attribute('innerHTML') 
        r2_3 = self.driver.find_element_by_xpath(self.r2).get_attribute('innerHTML') 
        sharpe_3 = self.driver.find_element_by_xpath(self.sharpe).get_attribute('innerHTML') 
        upside_3 = self.driver.find_element_by_xpath(self.upside).get_attribute('innerHTML') 
        downside_3 = self.driver.find_element_by_xpath(self.downside).get_attribute('innerHTML') 

        #navigate to 5 year section of Risk
        self.driver.find_element_by_xpath('//*[@id="for5Year"]').click() 
        sleep(3)
        r2_5 = self.driver.find_element_by_xpath(self.r2).get_attribute('innerHTML')
        sharpe_5 = self.driver.find_element_by_xpath(self.sharpe).get_attribute('innerHTML')
        upside_5 = self.driver.find_element_by_xpath(self.upside).get_attribute('innerHTML')
        downside_5 = self.driver.find_element_by_xpath(self.downside).get_attribute('innerHTML')

        # 10 year metrics
        #self.driver.find_element_by_xpath('//*[@id="'+id_tag+'"]/div/mds-button-group/div/slot/div/mds-button[3]/label/input').click()
        self.driver.find_element_by_xpath('//*[@id="for10Year"]').click()
        sleep(4)
        r2_10 = self.driver.find_element_by_xpath(self.r2).get_attribute('innerHTML')
        sharpe_10 = self.driver.find_element_by_xpath(self.sharpe).get_attribute('innerHTML')
        upside_10 = self.driver.find_element_by_xpath(self.upside).get_attribute('innerHTML')
        downside_10 = self.driver.find_element_by_xpath(self.downside).get_attribute('innerHTML')

        #Go to TDAmeritrade page, sleep for 2 seconds while it loads, grab 1, 3, 5, and 10 yr return and the date.
        self.driver.get(url_TD)
        sleep(4)

        return_1 = self.driver.find_element_by_xpath('//*[@id="table-trailingTotalReturnsTable"]/tbody/tr[4]/td[2]').get_attribute('innerHTML')
        return_3 = self.driver.find_element_by_xpath('//*[@id="table-trailingTotalReturnsTable"]/tbody/tr[5]/td[2]').get_attribute('innerHTML')
        return_5 = self.driver.find_element_by_xpath('//*[@id="table-trailingTotalReturnsTable"]/tbody/tr[6]/td[2]').get_attribute('innerHTML')
        return_10 = self.driver.find_element_by_xpath('//*[@id="table-trailingTotalReturnsTable"]/tbody/tr[7]/td[2]').get_attribute('innerHTML')

        # remove blank spaces from return numbers and clean up dirty sections from others.
        duration = ''.join(duration.split('<span class="mdc-data-point mdc-data-point--number" data-v-7ba8d775="" data-v-8645dbb6="">'))
        duration = ''.join(duration.split('</span>'))
        duration = ''.join(duration.split('years'))
        return_1 = ''.join(return_1.split('<span class="positive">'))
        return_1 = ''.join(return_1.split('%</span>'))
        return_1 = ''.join(return_1.split('<span class="negative">'))
        return_3 = ''.join(return_3.split('<span class="positive">'))
        return_3 = ''.join(return_3.split('<span class="negative">'))
        return_3 = ''.join(return_3.split('%</span>'))
        return_5 = ''.join(return_5.split('<span class="positive">'))
        return_5 = ''.join(return_5.split('%</span>'))
        return_5 = ''.join(return_5.split('<span class="negative">'))
        return_10 = ''.join(return_10.split('<span class="positive">'))
        return_10 = ''.join(return_10.split('%</span>'))
        return_10 = ''.join(return_10.split('<span class="negative">'))
        (	)
        	
        # create metric dictionary
        self.metric_dict = {
            # Organize and name rows for data.
            'Net Expense Ratio': net_expense,
            'Category': category,
            'TTM yield': TTMyield,
            'Effective duration': duration,
            '3 year Beta': beta_3,
            '3 Year Rsquare': r2_3,
            '3 Year Sharpe Ratio': sharpe_3,
            '3 Year Upside': upside_3,
            '3 Year downside': downside_3,
            '1 Year return': return_1,
            '3 Year return': return_3,
            '5 Year return': return_5,
            '10 Year return': return_10,

            ## 5 year
            '5 Year Rsquare': r2_5,
            '5 Year Sharpe Ratio': sharpe_5,
            '5 Year Upside': upside_5,
            '5 Year downside': downside_5,

            ## 10 year
            '10 Year Rsquare': r2_10,
            '10 Year Sharpe Ratio': sharpe_10,
            '10 Year Upside': upside_10,
            '10 Year downside': downside_10
        }

def fund_scrape(excel_path, csv_outputpath):

    #Calls the morningstar scrape bot and reads in tickers from excel sheet.

    try:
        # Import list from Excel Template
        excel_doc = xw.Book(f'{excel_path}')
        sheet = excel_doc.sheets['Bond Funds']

        # extract ticker list (from column A) as list. Selet if running first half or second half here:
        tickers = sheet.range('B:B').value
        tickers = [tick for tick in tickers if tick if tick != 'Ticker'] # if tick removes None values

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
        ticker_dict = dict(zip(tickers[0:50], metrics_list))
        ticker_df = pd.DataFrame.from_dict(ticker_dict)
        ticker_df.to_csv(csv_outputpath + '\\Bond_metrics.csv')
        # success
        print('The file was exported to the csv_outputpath as Bond_Metrics')

    except:
        print('The scrape did not run successfully')

fund_scrape(excel_path=r'F:\401K\User - Karsten\401k-ESOP-Canada\Fund Performance Review\Bond_tickers.xls', csv_outputpath='C:\Users\1341951\Desktop')


#VBMFX
