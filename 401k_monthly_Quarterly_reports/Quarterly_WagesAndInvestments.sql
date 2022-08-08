WITH Fund401k_Pivot AS (
--Pivot table to turn each fund into its own column. Sum for each fund for each SMID/SSN on plan and day. Replace Nulls with 0.
	SELECT plan_number, SSN, SMID, Calendar_day,SUM(ISNULL([0458-FID GOVT MMKT],0))AS MMKT ,SUM(ISNULL([2328-FID 500 INDEX],0)) AS Large_Cap
		,SUM(ISNULL([2352-FID MID CAP IDX],0)) AS Mid_Cap,SUM(ISNULL([2358-FID SM CAP IDX],0)) AS Small_Cap,SUM(ISNULL([2764-FID FDM IDX INC IPR],0)) AS Income
		,SUM(ISNULL([2765-FID FDM IDX 2005 IPR],0)) AS Tgt_2005, SUM(ISNULL([2766-FID FDM IDX 2010 IPR],0)) AS Tgt_2010,SUM(ISNULL([2767-FID FDM IDX 2015 IPR],0))AS Tgt_2015
		,SUM(ISNULL([2768-FID FDM IDX 2020 IPR],0)) AS Tgt_2020,SUM(ISNULL([2769-FID FDM IDX 2025 IPR],0)) AS Tgt_2025,SUM(ISNULL([2770-FID FDM IDX 2030 IPR],0)) AS Tgt_2030 
		,SUM(ISNULL([2771-FID FDM IDX 2035 IPR],0)) AS Tgt_2035,SUM(ISNULL([2772-FID FDM IDX 2040 IPR],0)) AS Tgt_2040,SUM(ISNULL([2773-FID FDM IDX 2045 IPR],0)) AS Tgt_2045
		,SUM(ISNULL([2774-FID FDM IDX 2050 IPR],0)) AS Tgt_2050,SUM(ISNULL([2775-FID FDM IDX 2055 IPR],0)) AS Tgt_2055,SUM(ISNULL([2776-FID FDM IDX 2060 IPR],0)) AS Tgt_2060
		,SUM(ISNULL([3427-FID FDM IDX 2065 IPR],0)) AS Tgt_2065,SUM(ISNULL([2834-FID TOTAL INTL IDX],0)) AS INTL, SUM(ISNULL([2944-FID TOTAL BOND K6],0)) AS Bonds
	--	,SUM(ISNULL([3704-MIP CL 2],0)),  SUM(ISNULL([SA2A-AMERCO STOCK],0))
--Subquery for data being pulled. Limit it to specific day and only 401k plan. No ESOP.
	from (SELECT *
	  FROM [DevRaw].[dbo].[Fund_Balances_n_CostBasis_EOM]
	  WHERE Calendar_day = '3/31/2022'
		AND Plan_number = '75951'
		) AS data_source
	PIVOT
	(
	  sum(market_value)
	  FOR Fund IN ([0458-FID GOVT MMKT],[2328-FID 500 INDEX],[2352-FID MID CAP IDX],[2358-FID SM CAP IDX],[2764-FID FDM IDX INC IPR],[2765-FID FDM IDX 2005 IPR],
		[2766-FID FDM IDX 2010 IPR],[2767-FID FDM IDX 2015 IPR],[2768-FID FDM IDX 2020 IPR],[2769-FID FDM IDX 2025 IPR],[2770-FID FDM IDX 2030 IPR],[2771-FID FDM IDX 2035 IPR],
		[2772-FID FDM IDX 2040 IPR],[2773-FID FDM IDX 2045 IPR],[2774-FID FDM IDX 2050 IPR],[2775-FID FDM IDX 2055 IPR],[2776-FID FDM IDX 2060 IPR],[3427-FID FDM IDX 2065 IPR],
		[2834-FID TOTAL INTL IDX],[2944-FID TOTAL BOND K6])
	) AS PVT
	GROUP BY Plan_number, SSN, SMID, Calendar_day
)

--This grabs information from the HCE monthly table. Will also calculate YTD numbers for people.
,HCE_Monthly AS (
SELECT Calendar_day, SMID,Historical_Status
	,DATEDIFF(MONTH, birth_date, Calendar_day)/12 AS HCE_AGE
	,Gross_Wages AS Monthly_Wages
	,Eligible_401K_Wages AS Monthly_Eligible
	,Roth_Contribution
	,PreTax_Contribution
	,Roth_Contribution + PreTax_Contribution AS Contribution_Monthly
	,Current_Roth_contribution_percentage 
	,Current_PreTax_contribution_percentage
	,Current_Roth_contribution_percentage + Current_PreTax_contribution_percentage AS Elected_Contribution_Perc
--Effective Contribution percentage. Amount contributed / Wages eligible. 
	,CASE WHEN Eligible_401K_Wages = 0 THEN 0
		ELSE ROUND(((Roth_Contribution + PreTax_Contribution) / Eligible_401K_Wages)*100,3) END AS Effective_Contribution_Perc_Monthly
--Repeat the above few lines, but be grabbing for YTD, not just month. First month and this will be the same.
	,SUM(Gross_Wages) OVER(PARTITION BY SMID, Year(calendar_Day) ORDER BY Calendar_Day) AS YTD_Gross_Wages
	,SUM(Eligible_401K_Wages) OVER(PARTITION BY SMID, Year(calendar_Day) ORDER BY Calendar_Day) AS YTD_401kEligible
	,SUM(PreTax_Contribution) OVER(PARTITION BY SMID, Year(calendar_Day) ORDER BY Calendar_Day) AS YTD_PreTax_Cont
	,SUM(Roth_Contribution) OVER(PARTITION BY SMID, Year(calendar_Day) ORDER BY Calendar_Day) AS YTD_Roth_Cont
	,SUM(PreTax_Contribution) OVER(PARTITION BY SMID, Year(calendar_Day) ORDER BY Calendar_Day) + SUM(Roth_Contribution) OVER(PARTITION BY SMID, Year(calendar_Day) ORDER BY Calendar_Day) AS YTD_Cont_total
	,CASE WHEN SUM(Eligible_401K_Wages) OVER(PARTITION BY SMID, Year(calendar_Day) ORDER BY Calendar_Day) = 0 THEN 0
		ELSE ROUND(SUM(PreTax_Contribution + Roth_Contribution) OVER(PARTITION BY SMID, Year(calendar_Day) ORDER BY Calendar_Day) 
			/ SUM(Eligible_401K_Wages) OVER(PARTITION BY SMID, Year(calendar_Day) ORDER BY Calendar_Day)*100,3) END AS YTD_Effective_Contribution_Perc
FROM [Workday].[dbo].[HCE_Determination_Monthly]
WHERE YEAR(Calendar_day) = YEAR('3/31/2022')
)

--From the prior CTE, add groups for wages, YTD wages, amount eligible, amount contribution. % effective contribution.
,HCE_M_Gouped AS (
SELECT Calendar_day ,SMID ,HCE_AGE ,Monthly_Wages ,Historical_Status AS Statuses
	,CASE WHEN Monthly_Wages < 800 THEN 'Under 800'
		WHEN Monthly_Wages BETWEEN 800 AND 2099.99 THEN '800 to 2099.99'
		WHEN Monthly_Wages BETWEEN 2100 AND 3299.99 THEN '2100 to 3299.99'
		WHEN Monthly_Wages BETWEEN 3300 AND 5399.99 THEN '3300 to 5399.99'
		WHEN Monthly_Wages BETWEEN 5400 AND 6699.99 THEN '5400 to 6699.99'
		WHEN Monthly_Wages BETWEEN 6700 AND 8299.99 THEN '6700 to 8299.99'
		WHEN Monthly_Wages > 8299.99 THEN '8300+'
		ELSE 'Missed' END AS Monthly_Wage_group
	,YTD_Gross_Wages
	,CASE WHEN YTD_Gross_Wages < 10000 THEN 'Under 10000'
		WHEN YTD_Gross_Wages BETWEEN 10000 and 24999.99 THEN '10k to 2499.99'
		WHEN YTD_Gross_Wages BETWEEN 25000 and 39999.99 THEN '25k to 39999.99'
		WHEN YTD_Gross_Wages BETWEEN 40000 and 64999.99 THEN '40k to 64999.99'
		WHEN YTD_Gross_Wages BETWEEN 65000 and 79999.99 THEN '65k to 79999.99'
		WHEN YTD_Gross_Wages BETWEEN 80000 and 99999.99 THEN '80k to 99999.99'
		WHEN YTD_Gross_Wages > 99999.99 THEN '100k+'
		ELSE 'Missed' END AS YTD_Wage_Group
	,Monthly_Eligible ,YTD_401kEligible ,CASE WHEN YTD_401kEligible < 10000 THEN 'Under 10000'
		WHEN YTD_401kEligible BETWEEN 10000 and 24999.99 THEN '10k to 2499.99'
		WHEN YTD_401kEligible BETWEEN 25000 and 39999.99 THEN '25k to 39999.99'
		WHEN YTD_401kEligible BETWEEN 40000 and 64999.99 THEN '40k to 64999.99'
		WHEN YTD_401kEligible BETWEEN 65000 and 79999.99 THEN '65k to 79999.99'
		WHEN YTD_401kEligible BETWEEN 80000 and 99999.99 THEN '80k to 99999.99'
		WHEN YTD_401kEligible > 99999.99 THEN '100k+'
		ELSE 'Missed' END AS YTD_401kEligible_Group
	,YTD_PreTax_Cont
	,YTD_Roth_Cont
	,YTD_Cont_total
	,CASE WHEN YTD_Cont_total = 0 THEN '0'
		WHEN YTD_Cont_total BETWEEN .01 AND 499.99 THEN '.01 to 499.99'
		WHEN YTD_Cont_total BETWEEN 500 and 999.99 THEN '500 to 999.99'
		WHEN YTD_Cont_total BETWEEN 1000 and 2499.99 THEN '1000 to 2499.99'
		WHEN YTD_Cont_total BETWEEN 2500 and 4999.99 THEN '2500 to 4999.99'
		WHEN YTD_Cont_total BETWEEN 5000 and 7499.99 THEN '5000 to 7499.99'
		WHEN YTD_Cont_total BETWEEN 7500 and 9999.99 THEN '7500 to 9999.99'
		WHEN YTD_Cont_total BETWEEN 10000 and 14999.99 THEN '10000 to 14999.99'
		WHEN YTD_Cont_total > 14999.99 THEN '15k+'
		ELSE 'Missed' END AS YTD_Cont_Group
	,Elected_Contribution_Perc
	,CASE WHEN Elected_Contribution_Perc = 0 THEN '0'
		WHEN Elected_Contribution_Perc BETWEEN .01 AND 1 THEN '.01 to 1'
		WHEN Elected_Contribution_Perc BETWEEN 1.01 and 2 THEN '1.01 to 2'
		WHEN Elected_Contribution_Perc BETWEEN 2.01 and 3 THEN '2.01 to 3'
		WHEN Elected_Contribution_Perc BETWEEN 3.01 and 5 THEN '3.01 to 5'
		WHEN Elected_Contribution_Perc BETWEEN 5.01 and 7 THEN '5.01 to 7'
		WHEN Elected_Contribution_Perc BETWEEN 7.01 and 9 THEN '7.01 to 9'
		WHEN Elected_Contribution_Perc > 9 THEN 'Over 9%'
		ELSE 'Missed' END AS Elected_Cont_Groups
	,YTD_Effective_Contribution_Perc
	,CASE WHEN Elected_Contribution_Perc = 0 THEN '0'
		WHEN YTD_Effective_Contribution_Perc BETWEEN .01 AND 1 THEN '.01 to 1'
		WHEN YTD_Effective_Contribution_Perc BETWEEN 1.01 and 2 THEN '1.01 to 2'
		WHEN YTD_Effective_Contribution_Perc BETWEEN 2.01 and 3 THEN '2.01 to 3'
		WHEN YTD_Effective_Contribution_Perc BETWEEN 3.01 and 5 THEN '3.01 to 5'
		WHEN YTD_Effective_Contribution_Perc BETWEEN 5.01 and 7 THEN '5.01 to 7'
		WHEN YTD_Effective_Contribution_Perc BETWEEN 7.01 and 9 THEN '7.01 to 9'
		WHEN YTD_Effective_Contribution_Perc > 9 THEN 'Over 9%'
		ELSE 'Missed' END AS YTD_Effective_Group
FROM HCE_Monthly
)

--CTE for ESOP funds. Only stocks, do not include cash. Will merge this with other CTEs so include smids and ssns. Calculate age in case person is only in ESOP and no wages or 401k balance.
,ESOP AS (
SELECT E.Calendar_day, E.SSN, E.Smid, /*DATEDIFF(MONTH, d.Birth_date, E.Calendar_day)/12 AS AGEs,d.Status_historical,*/ Fund, Market_value, Share_balance
/*	,CASE WHEN 
		WHEN
		ELSE '' END AS */
FROM [DevRaw].[dbo].[Fund_Balances_n_CostBasis_EOM] AS E
/*left join [DevRaw].[dbo].[Demographic_Data_EOM] AS D
	ON E.SSN = D.SSN
	AND E.Calendar_day = D.Calendar_day
	AND E.Plan_number = D.Plan_number*/
WHERE E.Plan_number = '75952'
	AND fund = 'SA2A-AMERCO STOCK'
	AND E.Calendar_day = '3/31/2022'
)

,FundPivot_ESOP AS (
SELECT COALESCE(fp.SSN, E.SSN) AS SSNs
	,COALESCE(fp.Calendar_day, e.Calendar_day) AS Calendar_Day
	,COALESCE(fp.smid ,e.smid) AS Smids
	,ISNULL(MMKT,0)MMKT ,ISNULL(Large_Cap,0)Large_Cap ,ISNULL(Mid_Cap,0)Mid_Cap ,ISNULL(Small_Cap,0)Small_Cap ,ISNULL(Income,0)Income ,ISNULL(INTL,0)INTL ,ISNULL(Bonds,0)Bonds
	,ISNULL(Tgt_2005,0)Tgt_2005 ,ISNULL(Tgt_2010,0)Tgt_2010 ,ISNULL(Tgt_2015,0)Tgt_2015 ,ISNULL(Tgt_2020,0)Tgt_2020 ,ISNULL(Tgt_2025,0) Tgt_2025,ISNULL(Tgt_2030,0)Tgt_2030 ,ISNULL(Tgt_2035,0)Tgt_2035
	,ISNULL(Tgt_2040,0)Tgt_2040 ,ISNULL(Tgt_2045,0)Tgt_2045 ,ISNULL(Tgt_2050,0)Tgt_2050 ,ISNULL(Tgt_2055,0)Tgt_2055 ,ISNULL(Tgt_2060,0)Tgt_2060 ,ISNULL(Tgt_2065,0)Tgt_2065
	,ISNULL(Market_value,0) AS ESOP_Value ,ISNULL(Share_balance,0) AS Esop_Shares
FROM Fund401k_Pivot AS FP
FULL JOIN ESOP AS E
	ON FP.SSN = E.SSN
	AND FP.Calendar_day = e.Calendar_day
)

--,HCE_and_401k_and_ESOP AS (
SELECT COALESCE (fpe.Smids,h.smid) AS SMIDs
	,fpe.SSNs
	,COALESCE (fpe.Smids,h.smid,fpe.SSNs) AS IDs
	,h.Statuses
	,COALESCE (FPe.Calendar_day,h.Calendar_day) AS Calendar_Days
	,COALESCE (DATEDIFF(MONTH, d.Birth_date, FPE.Calendar_day)/12 ,h.HCE_AGE) AS AGEs
--	,COALESCE(HCE_AGE,DATEDIFF(MONTH, d.Birth_date, FP.Calendar_day)/12) AS AGEs
	,Monthly_Eligible
	,YTD_Gross_Wages
	,YTD_401kEligible
	,YTD_PreTax_Cont 
	,YTD_Roth_Cont 
	,h.YTD_Effective_Contribution_Perc
	,h.Elected_Cont_Groups
	,h.Monthly_Wage_group
	,h.YTD_401kEligible_Group
	,h.YTD_Cont_Group
	,h.YTD_Effective_Group
	,h.YTD_Wage_Group
/*	,ISNULL(MMKT,0) + ISNULL(Large_Cap,0) + ISNULL(Mid_Cap,0)+ISNULL(Small_Cap,0)+ISNULL(Income,0)+ISNULL(INTL,0)+ISNULL(Bonds,0)+
		ISNULL(Tgt_2005,0)+ISNULL(Tgt_2010,0)+ISNULL(Tgt_2015,0)+ISNULL(Tgt_2020,0)+ISNULL(Tgt_2025,0)+ISNULL(Tgt_2030,0)+ISNULL(Tgt_2035,0)+ISNULL(Tgt_2040,0)+
		ISNULL(Tgt_2045,0)+ISNULL(Tgt_2050,0)+ISNULL(Tgt_2055,0)+ISNULL(Tgt_2060,0)+ISNULL(Tgt_2065,0) AS Funds401k*/
	,(MMKT+ Large_Cap+ Mid_Cap+Small_Cap+Income+INTL+Bonds
		+Tgt_2005+Tgt_2010+Tgt_2015+Tgt_2020+Tgt_2025+Tgt_2030+Tgt_2035+Tgt_2040
		+Tgt_2045+Tgt_2050+Tgt_2055+Tgt_2060+Tgt_2065) AS Total_401kFunds
	,fpe.ESOP_Value
	,fpe.Esop_Shares
FROM FundPivot_ESOP  AS FPE
FULL JOIN HCE_M_Gouped AS H
	ON FPE.Smids = H.SMID
	AND FPE.Calendar_Day = h.Calendar_day
LEFT JOIN [DevRaw].[dbo].[Demographic_Data_EOM] AS D
	ON FPE.Calendar_day = d.Calendar_day
	AND FPE.SSNs = D.SSN
WHERE COALESCE (FPe.Calendar_day,h.Calendar_day) = '3/31/2022'
--)*/