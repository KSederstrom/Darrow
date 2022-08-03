# Written by 1263298. Last modified 2/5/2021.

import pandas as pd
import win32com.client as win32
excel = win32.gencache.EnsureDispatch("Excel.Application")



############################################################################
#This section changes xlsx to csv if needed.

# Open xlsx Workbook from saved location above and saves as a CSV
xlwb = excel.Workbooks.Open(r"C:\Users\1263298\Desktop\Python\ESOPDumpTest\DumpExcel\SMID-X.xlsx")
xlwb.SaveAs(r"C:\Users\1263298\Desktop\Python\ESOPDumpTest\DumpCSV\SMID-X.csv", 24)
xlwb.Close(False)

# Open xlsx Workbook from saved location above and saves as a CSV
xlwb = excel.Workbooks.Open(r"C:\Users\1263298\Desktop\Python\ESOPDumpTest\DumpExcel\SMID-X2.xlsx")
xlwb.SaveAs(r"C:\Users\1263298\Desktop\Python\ESOPDumpTest\DumpCSV\SMID-X2.csv", 24)
xlwb.Close(False)


#############################################################################
#This reads in an excel file for the validation

data_dump= pd.read_excel(r"C:\Users\1263298\Desktop\Python\ESOPDumpTest\DumpExcel\SMID-1.xlsx")
eligibility_criteria = pd.read_excel(r'C:\Users\1263298\Desktop\Python\Eligibility.xlsx', sheet_name="Sheet1")

# Defining function to call later for eligibility
def filter_eligibility(row,component,include):
    if component in row["Component"]:
        if include == row["Included"]:
            return True
        else:
            return False
    else:
        return False

# Subsetting Columns, purpose is to take the SMIDs and specific columns out of the main data.
vars_1 =['SMID', 'Pay Date', 'Employee Type', 'Pay Frequency', 'Sub Period From', 'Sub Period To']
smid_group = data_dump[vars_1].copy()
smid_group.head()
smid_group['Pay Date'] = pd.to_datetime(smid_group['Pay Date'])


#############################################################################
# Hours Portion


# Combining the set of columns headings just created with the actual data, and then combining with the first part
hours_group = [placeholder for placeholder in data_dump.columns if "hours" in placeholder.lower()]
hours_group.insert(0, "SMID")
print(hours_group)
hours_dump = data_dump[hours_group]

# Sidenote: Left_index and right_index needed for repeating values
hours_combine = pd.merge(smid_group, hours_dump, left_index=True, right_index=True, on="SMID")
hours_combine.shape
print(hours_combine.columns)
hours_group_by = hours_combine.groupby("SMID")
hours_sum = hours_group_by.sum()
hours_final = hours_sum.reset_index()
print(hours_final)

# This checks to see what is considered Eligible Hours/Wages
all_eligible = eligibility_criteria.query("Included=='Yes'")
print(all_eligible)

# This uses the prior function to filter out only the eligible components
# Eligible Hours
hoursyes = eligibility_criteria[eligibility_criteria.apply(lambda x:filter_eligibility(x,"Hours","Yes"), axis=1)]
hoursyes = list(hoursyes["Component"].values)
hoursyes.insert(0, "SMID")
hoursyes_final = hours_final[hoursyes].copy()
hoursyes_final["Sum of Eligible Hours"] = hoursyes_final.apply(lambda x: x.iloc[1:].sum(),axis=1)
print(hoursyes_final)

# Ineligible Hours
hoursno = eligibility_criteria[eligibility_criteria.apply(lambda x:filter_eligibility(x,"Hours","No"), axis=1)]
hoursno = list(hoursno["Component"].values)
hoursno.insert(0, "SMID")
hoursno_final = hours_final[hoursno].copy()
hoursno_final["Sum of Ineligible Hours"] = hoursno_final.apply(lambda x: x.iloc[1:].sum(),axis=1)
print(hoursno_final)


vars_2 = ["SMID","Sum of Eligible Hours"]
vars_3 = ["SMID","Sum of Ineligible Hours"]
hours_complete = hoursyes_final[vars_2].copy()
hours_partial = hoursno_final[vars_3].copy()
print(hours_partial)
hours_complete = hours_complete.merge(hours_partial)
print(hours_complete)

#############################################################################
# Wages Portion.

wages_group = [placeholder for placeholder in data_dump.columns if "wages" in placeholder.lower()]
wages_group.insert(0, "SMID")
print(wages_group)
wages_dump = data_dump[wages_group]
wages_combine = pd.merge(smid_group, wages_dump, left_index=True, right_index=True, on="SMID")

# Data was reading in as strings w/ commas. Removing commas and converting to floats
for column in wages_combine.columns[6:]: 
    wages_combine[column] = wages_combine[column].apply(lambda x: float(str(x).replace(",", "")))
wages_combine.shape
print(wages_combine.columns)

wages_group_by = wages_combine.groupby("SMID",as_index=False)
wages_sum = wages_group_by.sum()
wages_final = wages_sum.reset_index()
print(wages_final)

for column in wages_final.columns:
    if "dontuse" in column.lower():
        print(column)

#Eligible Wages
wagesyes = eligibility_criteria[eligibility_criteria.apply(lambda x:filter_eligibility(x,"Wages","Yes"), axis=1)]
wagesyes = list(wagesyes["Component"].values)
wagesyes.insert(0, "SMID")
wagesyes_final = wages_final[wagesyes].copy()
wagesyes_final["Sum of Eligible Wages"] = wagesyes_final.apply(lambda x: x.iloc[1:].sum(),axis=1)
print(wagesyes_final)

#Ineligible Wages
wagesno = eligibility_criteria[eligibility_criteria.apply(lambda x:filter_eligibility(x,"Wages","No"), axis=1)]
wagesno = list(wagesno["Component"].values)
wagesno.insert(0, "SMID")
print(wagesno)
wagesno_final = wages_final[wagesno].copy()
wagesno_final["Sum of Ineligible Wages"] = wagesno_final.apply(lambda x: x.iloc[1:].sum(),axis=1)
print(wagesno_final)

vars_4 = ["SMID","Sum of Eligible Wages"]
vars_5 = ["SMID","Sum of Ineligible Wages"]
wages_complete = wagesyes_final[vars_4].copy()
wages_partial = wagesno_final[vars_5].copy()
print(wages_partial)
wages_complete = wages_complete.merge(wages_partial)
print(wages_complete)

#############################################################################
# Merging Final Hours and Wages


partial_final = pd.merge(hours_final,wages_final,on="SMID")
partial_final.to_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/Breakdown-XX"
                          r".xlsx", sheet_name="Sheet A", index=False)


project_complete = wages_complete.merge(hours_complete)
print(project_complete)
list(project_complete)
print("Finished")
project_complete.to_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/PySMID-XX"
                          r".xlsx", sheet_name="Sheet A", index=False)

#############################################################################
# Ouputs Combining

df1 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/PySMID-1"
                          r".xlsx", sheet_name="Sheet A", index=False)
df2 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/PySMID-2"
                          r".xlsx", sheet_name="Sheet A", index=False)
df3 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/PySMID-3"
                          r".xlsx", sheet_name="Sheet A", index=False)
df4 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/PySMID-4"
                          r".xlsx", sheet_name="Sheet A", index=False)
df5 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/PySMID-5"
                          r".xlsx", sheet_name="Sheet A", index=False)
df6 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/PySMID-6"
                          r".xlsx", sheet_name="Sheet A", index=False)
df7 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/PySMID-7"
                          r".xlsx", sheet_name="Sheet A", index=False)
df8 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/PySMID-8"
                          r".xlsx", sheet_name="Sheet A", index=False)
df9 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/PySMID-9"
                          r".xlsx", sheet_name="Sheet A", index=False)
df10 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/PySMID-10"
                          r".xlsx", sheet_name="Sheet A", index=False)
df11 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/PySMID-11"
                          r".xlsx", sheet_name="Sheet A", index=False)
df12 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/PySMID-12"
                          r".xlsx", sheet_name="Sheet A", index=False)
df13 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/PySMID-13"
                          r".xlsx", sheet_name="Sheet A", index=False)
df14 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/PySMID-14"
                          r".xlsx", sheet_name="Sheet A", index=False)
df15 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/PySMID-15"
                          r".xlsx", sheet_name="Sheet A", index=False)
df16 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/PySMID-16"
                          r".xlsx", sheet_name="Sheet A", index=False)
df17 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/PySMID-17"
                          r".xlsx", sheet_name="Sheet A", index=False)
df18 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/PySMID-18"
                         r".xlsx", sheet_name="Sheet A", index=False)
# df19 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOP Dump Test/SMID-19"
#                          r".xlsx", sheet_name="Sheet A", index=False)
# df20 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOP Dump Test/SMID-20"
#                          r".xlsx", sheet_name="Sheet A", index=False)
# df21 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOP Dump Test/SMID-21"
#                          r".xlsx", sheet_name="Sheet A", index=False)

Final_Project = pd.concat([df1,df2,df3,df4,df5,df6,df7,df8,df9,df10,df11,df12,df13,df14,df15,df16,df17,df18], ignore_index=True,sort=False)
Final_Project.to_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/Combined_SMIDs_2.xlsx", sheet_name="Sheet A", index=False)


dfx1 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/Breakdown-1"
                          r".xlsx", sheet_name="Sheet A", index=False)
dfx2 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/Breakdown-2"
                          r".xlsx", sheet_name="Sheet A", index=False)
dfx3 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/Breakdown-3"
                          r".xlsx", sheet_name="Sheet A", index=False)
dfx4 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/Breakdown-4"
                          r".xlsx", sheet_name="Sheet A", index=False)
dfx5 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/Breakdown-5"
                          r".xlsx", sheet_name="Sheet A", index=False)
dfx6 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/Breakdown-6"
                          r".xlsx", sheet_name="Sheet A", index=False)
dfx7 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/Breakdown-7"
                          r".xlsx", sheet_name="Sheet A", index=False)
dfx8 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/Breakdown-8"
                          r".xlsx", sheet_name="Sheet A", index=False)
dfx9 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/Breakdown-9"
                          r".xlsx", sheet_name="Sheet A", index=False)
dfx10 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/Breakdown-10"
                          r".xlsx", sheet_name="Sheet A", index=False)
dfx11 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/Breakdown-11"
                          r".xlsx", sheet_name="Sheet A", index=False)
dfx12 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/Breakdown-12"
                          r".xlsx", sheet_name="Sheet A", index=False)
dfx13 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/Breakdown-13"
                          r".xlsx", sheet_name="Sheet A", index=False)
dfx14 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/Breakdown-14"
                          r".xlsx", sheet_name="Sheet A", index=False)
dfx15 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/Breakdown-15"
                          r".xlsx", sheet_name="Sheet A", index=False)
dfx16 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/Breakdown-16"
                          r".xlsx", sheet_name="Sheet A", index=False)
dfx17 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/Breakdown-17"
                          r".xlsx", sheet_name="Sheet A", index=False)
dfx18 = pd.read_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/Breakdown-18"
                         r".xlsx", sheet_name="Sheet A", index=False)

#Final Breakdown
Final_Breakdown = pd.concat([dfx1,dfx2,dfx3,dfx4,dfx5,dfx6,dfx7,dfx8,dfx9,dfx10,dfx11,dfx12,dfx13,dfx14,dfx15,dfx16
                                ,dfx17,dfx18], ignore_index=True,sort=False)
Final_Breakdown.to_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/Final-Breakdown-2020.xlsx", sheet_name="Sheet A",
                         index=False)

#Individual Breakdowns
partial_final.to_excel(r"C:/Users/1263298/Desktop/Python/ESOPDumpTest/Breakdown-18"
                          r".xlsx", sheet_name="Sheet A", index=False)