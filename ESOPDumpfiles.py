import pyodbc
import sqlalchemy
import urllib
import pandas as pd
import sys
from datetime import date

#Set the calling procedure and retrieve process metadata
sys.path.append(r'\\nacl01fs01prd.uhaul.amerco.org\401K\Fidelity\IT\Python Scripts\Karsten')

import Retirement_benefit_metadata_master
calling_procedure = "ESOPDumps"
batch_id = Retirement_benefit_metadata_master.initialize_metadata(calling_procedure)

#lines to connect to the SQL server database
base_sql=("Driver=ODBC Driver 17 for SQL Server;"
          "Server= hrsDbsSqlwP0003.uhaul.amerco.org;"
          "database=DevRaw;"
          "Trusted_Connection=yes;"
          )
con_sql= pyodbc.connect(base_sql)

#lines 16,17 are needed to upload data into SQL server.
params_sql=urllib.parse.quote_plus(base_sql)
engine_sql=sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params_sql)

#lines to read_csv or read_xlsx from a shared drive file path
file_df=pd.read_csv(r'\\nacl01fs01prd.uhaul.amerco.org\401K\User - Karsten\401k-ESOP-Canada\Allocation Validation ESOP\2022-03-30\Dumps\paymentlogdump_1083155_thru_1152101_03302022.csv')
#file_df=pd.read_csv(r'\\nacl01fs01prd.uhaul.amerco.org\HRFS02\HR\#401K\User - Karsten\401k-ESOP-Canada Links\Allocation Validation ESOP\2022-01-17\Dumps\paymentlogdump_1033080_thru_1083688_01152022.csv')

# Delete the Time and Zone columns, not needed anymore. Also delete the initial sign column.
file_df.drop('Additional Compensation Hours',axis = 1, inplace = True)
file_df.drop('AFM PCP Hours',axis = 1, inplace = True)
file_df.drop('AFM PCP_Dontuse Hours',axis = 1, inplace = True)
file_df.drop('Annual GM PCP Hours',axis = 1, inplace = True)
file_df.drop('Bonus Pay (Gross Up) Hours',axis = 1, inplace = True)
file_df.drop('Bonus Pay (Non Cash Taxable) Hours',axis = 1, inplace = True)
file_df.drop('Bonus Pay (Non Cash Taxable)_Dontuse Hours',axis = 1, inplace = True)
file_df.drop('Bonus Pay (Regular) Hours',axis = 1, inplace = True)
file_df.drop('Bonus Pay (Regular)_Dontuse Hours',axis = 1, inplace = True)
file_df.drop('Cash Incentive (Non Cash Taxable) Hours',axis = 1, inplace = True)
file_df.drop('Cash Incentive (Non Cash Taxable)_Dontuse Hours',axis = 1, inplace = True)
file_df.drop('Cash Incentive (Regular) Hours',axis = 1, inplace = True)
file_df.drop('Cash Incentive (Regular)_Dontuse Hours',axis = 1, inplace = True)
file_df.drop('Center PCP Hours',axis = 1, inplace = True)
file_df.drop('Center PCP_Dontuse Hours',axis = 1, inplace = True)
file_df.drop('CMPY SSA Hours',axis = 1, inplace = True)
file_df.drop('Co Vehicle Hours',axis = 1, inplace = True)
file_df.drop('Collector PCP Hours',axis = 1, inplace = True)
file_df.drop('Contact Center Bon Hours',axis = 1, inplace = True)
file_df.drop('Contact Center Bon_Dontuse Hours',axis = 1, inplace = True)
file_df.drop('Discr Bonus (Gross Up) Hours',axis = 1, inplace = True)
file_df.drop('Discr Bonus (Non Cash Taxable) Hours',axis = 1, inplace = True)
file_df.drop('Discr Bonus (Non Cash Taxable)_Dontuse Hours',axis = 1, inplace = True)
file_df.drop('Discr Bonus (Regular) Hours',axis = 1, inplace = True)
file_df.drop('Discr Bonus DontUse (Regular) Hours',axis = 1, inplace = True)
file_df.drop('EMGY Personal Payoff Hours',axis = 1, inplace = True)
file_df.drop('Gifts & Awards Hours',axis = 1, inplace = True)
file_df.drop('Gifts & Awards_Dontuse Hours',axis = 1, inplace = True)
file_df.drop('GM Additional Compensation Hours',axis = 1, inplace = True)
file_df.drop('GM PCP Hours',axis = 1, inplace = True)
file_df.drop('GM PCP_Dontuse Hours',axis = 1, inplace = True)
file_df.drop('Hitch Bonus Hours',axis = 1, inplace = True)
file_df.drop('MCP PCP Hours',axis = 1, inplace = True)
file_df.drop('MCP PCP_Dontuse Hours',axis = 1, inplace = True)
file_df.drop('New Hire Bonus from POS-US Hours',axis = 1, inplace = True)
file_df.drop('Occup Bonus Hours',axis = 1, inplace = True)
file_df.drop('Real Est Bonus Hours',axis = 1, inplace = True)
file_df.drop('Real Est Bonus-Dontuse Hours',axis = 1, inplace = True)
file_df.drop('Res Mgr PCP Hours',axis = 1, inplace = True)
file_df.drop('Res Mgr PCP_Dontuse Hours',axis = 1, inplace = True)
file_df.drop('Sales Bonus Hours',axis = 1, inplace = True)
file_df.drop('Sales Bonus_Dontuse Hours',axis = 1, inplace = True)
file_df.drop('Severance Pay Hours',axis = 1, inplace = True)
file_df.drop('Severance Pay_Dontuse Hours',axis = 1, inplace = True)
file_df.drop('SM/SS PCP Hours',axis = 1, inplace = True)
file_df.drop('SOAR Bonus Hours',axis = 1, inplace = True)
file_df.drop('SOAR Bonus_Dontuse Hours',axis = 1, inplace = True)
file_df.drop('Special Bonus (Regular) Hours',axis = 1, inplace = True)
file_df.drop('SSA _Activity Hours',axis = 1, inplace = True)
file_df.drop('SSA _Front Load Hours',axis = 1, inplace = True)
file_df.drop('SSA _Special Contribution Hours',axis = 1, inplace = True)
file_df.drop('SSA _Wellness Hours',axis = 1, inplace = True)
file_df.drop('SSA MTCH Hours',axis = 1, inplace = True)
file_df.drop('Storage PCP 1 Hours',axis = 1, inplace = True)
file_df.drop('Storage PCP 1_Dontuse Hours',axis = 1, inplace = True)
file_df.drop('Traffic PCP Hours',axis = 1, inplace = True)
file_df.drop('Traffic PCP_Dontuse Hours',axis = 1, inplace = True)
file_df.drop('Truck Sales Hours',axis = 1, inplace = True)
file_df.drop('UBOX Bonus Hours',axis = 1, inplace = True)

#Force in the date of the file. Manually change!!!
file_date = '2022-03-30'
file_df.columns
file_df['File Date'] = file_date

#Add a column for batch ids.
file_df.columns
file_df ['batch_id'] = batch_id

print(file_df.columns)

#lines to upload the dataframe into SQL table
file_df.to_sql("ESOPDumps",engine_sql, if_exists="append",index=False)
# Finalze batch_Id and Metadata
Retirement_benefit_metadata_master.finalize_metadata(batch_id)

csv_outputpath=r'F:\401K\User - Karsten\401k-ESOP-Canada\Allocation Validation ESOP\2022-03-30\SQL Cleaned'
file_df.to_csv(csv_outputpath + '\\Dump 3.csv')

# print Finish to make it easier to see if done.
print ('finished')

