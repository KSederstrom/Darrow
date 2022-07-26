import pyodbc
import pandas as pd
import xlwings as xw
from bs4 import BeautifulSoup
import os
from datetime import datetime
from time import sleep

excel_outputpath=r'F:\401K\1. 401K & ESOP\User - Karsten\Alex monthly\Monthly Trend analysis template V1.21 (updated 2022.07.03).xlsx'
Runtime = '2022.06.28'
#Loan_df.to_excel(excel_outputpath + '\Loans_' + Runtime + '.xlsx')
#Connect to SQL, you can read SQL from just those lines
base_sql=("Driver=ODBC Driver 17 for SQL Server;"
          "Server= hrsDbsSqlwP0003.uhaul.amerco.org;"
          "database=DevRaw;"
          "Trusted_Connection=yes;"
          )
con_sql= pyodbc.connect(base_sql)

#Grab information for the monthly 401k reports from SQL using views, put them into excel based on tba names. 
#Include order by manually at the bottom if wanted.

#------------------------------------------------------------------
#SQL_Fund_Changes
SqlFundchangesQuery ="""
SELECT *
FROM [DevRaw].[dbo].[Monthly_Fund_Changes]
ORDER BY EndOMonth desc
"""

#grab from SQL into pandas DF
FundChanges_df=pd.read_sql_query (SqlFundchangesQuery ,con_sql)

#Print if want to review
#print (FundChanges_df)

#Save as csv
wb = xw.Book(excel_outputpath)
query_sheetFC = wb.sheets["SQL_Fund_Changes"]
query_sheetFC.range("1:25000").clear()
query_sheetFC.range("A1").options(index=False).value = FundChanges_df
sleep(2)
#query_sheet.Visible = 1

#------------------------------------------------------------------
#SQL_Asset_Allocation
SqlAAQuery ="""
SELECT *
FROM [DevRaw].[dbo].[Monthly_Asset_Allocation]
ORDER BY Calendar_day desc
"""

#grab from SQL into pandas DF
AA_df=pd.read_sql_query (SqlAAQuery ,con_sql)

#Print if want to review
#print (AA_df)

#Save as csv
wb = xw.Book(excel_outputpath)
query_sheetAA = wb.sheets["SQL_Asset_Allocation"]
query_sheetAA.range("1:25000").clear()
query_sheetAA.range("A1").options(index=False).value = AA_df
sleep(2)
#query_sheet.Visible = 1

#------------------------------------------------------------------
#SQL_Cont_Act
SqlContributionQuery ="""
SELECT *
FROM [DevRaw].[dbo].[Monthly_Contribution_Activity]
ORDER BY EndOMonth desc
	,source
"""

#grab from SQL into pandas DF
Contribution_df=pd.read_sql_query (SqlContributionQuery ,con_sql)

#Print if want to review
#print (Contribution_df)

#Save as csv
wb = xw.Book(excel_outputpath)
query_sheetCA = wb.sheets["SQL_Cont_Act"]
query_sheetCA.range("1:25000").clear()
query_sheetCA.range("A1").options(index=False).value = Contribution_df
sleep(5)
#query_sheet.Visible = 1

#------------------------------------------------------------------
#SQL_Deferral

#------------------------------------------------------------------
#SQL_Dist_Info part 1
SqlDistribution1Query ="""
SELECT *
FROM [DevRaw].[dbo].[Monthly_Distribution_Info]
ORDER BY MonthEnd desc
	,transaction_type asc
	,Withdrawal_description desc
"""

#grab from SQL into pandas DF
Distribution1_df=pd.read_sql_query (SqlDistribution1Query ,con_sql)

#Print if want to review
#print (Distribution1_df)

#Save as csv
wb = xw.Book(excel_outputpath)
query_sheetDI = wb.sheets["SQL_Dist_Info"]
query_sheetDI.range("1:25000").clear()
query_sheetDI.range("A1").options(index=False).value = Distribution1_df
sleep(2)
#query_sheet.Visible = 1

#------------------------------------------------------------------
#SQL_Dist_Info part 2 Outstanding Loans
SqlOutstandingLoanQuery ="""
SELECT EOMONTH(Calendar_day) AS EndOMonth
	,COUNT (Distinct SSN) AS CountUniqueSSNs
	,SUM(Outstanding_balance) AS TotalOutstandingLoan
	,AVG(Outstanding_balance) AS AvgOutstanding
FROM [DevRaw].[dbo].[LoanBalances_EOM]
GROUP BY EOMonth(calendar_day)
ORDER BY EOMonth(calendar_day) desc
"""

#grab from SQL into pandas DF
OutstandingLoan_df=pd.read_sql_query (SqlOutstandingLoanQuery ,con_sql)

#Print if want to review
#print (Distribution1_df)

#Save as csv
wb = xw.Book(excel_outputpath)
query_sheetOL = wb.sheets["SQL_Dist_Info"]
query_sheetOL.range("T1").options(index=False).value = OutstandingLoan_df
sleep(2)
#query_sheet.Visible = 1

#------------------------------------------------------------------
#SQL_Fund_Balances
SqlFundBalancesQuery ="""
SELECT *
FROM [DevRaw].[dbo].[Monthly_Fund_Balances]
ORDER BY Calendar_day desc
	,Fund desc
	,AgeGroup ASC
	,Identifier 
"""

#grab from SQL into pandas DF
FundBalances_df=pd.read_sql_query (SqlFundBalancesQuery ,con_sql)

#Print if want to review
#print (InvestElection_df)

#Save as csv
wb = xw.Book(excel_outputpath)
query_sheetFB = wb.sheets["SQL_Fund_Balances"]
query_sheetFB.range("1:25000").clear()
query_sheetFB.range("A1").options(index=False).value = FundBalances_df
sleep(5)
#query_sheet.Visible = 1

#------------------------------------------------------------------
#SQL_Invest_Election
SqlInvestElectionQuery ="""
SELECT *
 FROM [DevRaw].[dbo].[Monthly_Investment_Elections]
 ORDER BY Calendar_day desc, fund desc
"""

#grab from SQL into pandas DF
InvestElection_df=pd.read_sql_query (SqlInvestElectionQuery ,con_sql)

#Print if want to review
#print (InvestElection_df)

#Save as csv
wb = xw.Book(excel_outputpath)
query_sheetIE = wb.sheets["SQL_Invest_Election"]
query_sheetIE.range("1:25000").clear()
query_sheetIE.range("A1").options(index=False).value = InvestElection_df
sleep(2)
#query_sheet.Visible = 1
