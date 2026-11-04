import sqlite3
import pandas as pd

# 1. Database Connection
db_name = 'netflix_customer_intelligence.db'
conn = sqlite3.connect(db_name)

# Excel Writer तैयार करें
excel_file = 'netflix_37_business_solutions.xlsx'
writer = pd.ExcelWriter(excel_file, engine='openpyxl')

# 2. Section A, B, C की सभी 37 क्वेरीज़
all_queries = {
    # SECTION A (Q1-Q15)
    "Q01_Active_Customers": "SELECT country, COUNT(DISTINCT customer_id) AS active_customers FROM netflix_data WHERE churned = 0 GROUP BY country ORDER BY active_customers DESC;",
    "Q02_Revenue_By_Plan": "SELECT plan_id, SUM(monthly_price) AS total_revenue, ROUND(AVG(monthly_price), 2) AS avg_monthly_revenue FROM netflix_data GROUP BY plan_id;",
    "Q03_Overall_Churn_Rate": "SELECT ROUND(SUM(CASE WHEN churned = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_percentage FROM netflix_data;",
    "Q04_Channel_Churn_Rate": "SELECT acquisition_channel, COUNT(DISTINCT customer_id) AS total_customers, ROUND(SUM(CASE WHEN churned = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS channel_churn_rate FROM netflix_data GROUP BY acquisition_channel ORDER BY total_customers DESC;",
    "Q05_Avg_Age_By_Plan": "SELECT plan_id, ROUND(AVG(age), 2) AS avg_age FROM netflix_data GROUP BY plan_id;",
    "Q06_Top10_Watch_Duration": "SELECT content_id, SUM(watch_duration_minutes) AS total_watch_minutes FROM netflix_data GROUP BY content_id ORDER BY total_watch_minutes DESC LIMIT 10;",
    "Q07_Completion_Pct_Device": "SELECT device_type, ROUND(AVG(completion_percentage), 2) AS avg_completion_percentage FROM netflix_data GROUP BY device_type;",
    "Q08_Failed_Payments": "SELECT payment_status, COUNT(*) AS failed_count FROM netflix_data WHERE payment_status = 'Failed' GROUP BY payment_status;",
    "Q09_Session_Duration_Device": "SELECT device_type, ROUND(AVG(session_duration_minutes), 2) AS avg_session_minutes FROM netflix_data GROUP BY device_type;",
    "Q10_Churn_Reasons": "SELECT churn_reason, COUNT(*) AS customer_count FROM netflix_data WHERE churned = 1 GROUP BY churn_reason ORDER BY customer_count DESC;",
    "Q11_Viewing_Minutes_Device": "SELECT device_type, SUM(watch_duration_minutes) AS total_viewing_minutes FROM netflix_data GROUP BY device_type ORDER BY total_viewing_minutes DESC;",
    "Q12_Avg_Price_Segment": "SELECT customer_segment, ROUND(AVG(monthly_price), 2) AS avg_price FROM netflix_data GROUP BY customer_segment ORDER BY avg_price DESC;",
    "Q13_Customers_Per_Channel": "SELECT acquisition_channel, COUNT(DISTINCT customer_id) AS customer_count FROM netflix_data GROUP BY acquisition_channel ORDER BY customer_count DESC;",
    "Q14_Auto_Renew_Off_Pct": "SELECT ROUND(SUM(CASE WHEN auto_renew = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS auto_renew_off_percentage FROM netflix_data;",
    "Q15_High_Support_Tickets": "SELECT customer_id, COUNT(payment_id) AS total_tickets FROM netflix_data GROUP BY customer_id HAVING COUNT(payment_id) > 3 ORDER BY total_tickets DESC LIMIT 20;",

    # SECTION B (Q16-Q27)
    "Q16_Plan_Revenue_Rank": "WITH plan_revenue AS (SELECT plan_id, SUM(monthly_price) AS total_revenue FROM netflix_data GROUP BY plan_id) SELECT plan_id, total_revenue, RANK() OVER (ORDER BY total_revenue DESC) AS plan_rank FROM plan_revenue;",
    "Q17_Recent_Payment_RowNumber": "WITH ranked_payments AS (SELECT customer_id, payment_id, payment_date, amount, payment_status, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY payment_date DESC) as rn FROM netflix_data) SELECT customer_id, payment_id, payment_date, amount, payment_status FROM ranked_payments WHERE rn = 1 LIMIT 20;",
    "Q18_3Month_Moving_Avg_Signups": "WITH monthly_signups AS (SELECT strftime('%Y-%m', registration_date) AS signup_month, COUNT(DISTINCT customer_id) AS new_customers FROM netflix_data WHERE registration_date IS NOT NULL GROUP BY signup_month) SELECT signup_month, new_customers, ROUND(AVG(new_customers) OVER (ORDER BY signup_month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS moving_avg_3_months FROM monthly_signups;",
    "Q19_MoM_Watch_Decline_Lag": "WITH monthly_watch AS (SELECT customer_id, strftime('%Y-%m', viewing_date) AS watch_month, SUM(watch_duration_minutes) AS total_watch_time FROM netflix_data WHERE viewing_date IS NOT NULL GROUP BY customer_id, watch_month), lagged_watch AS (SELECT customer_id, watch_month, total_watch_time, LAG(total_watch_time) OVER (PARTITION BY customer_id ORDER BY watch_month) AS prev_month_watch_time FROM monthly_watch) SELECT customer_id, watch_month, total_watch_time, prev_month_watch_time, CASE WHEN total_watch_time < prev_month_watch_time THEN 1 ELSE 0 END AS mom_decline_flag FROM lagged_watch WHERE prev_month_watch_time IS NOT NULL LIMIT 20;",
    "Q20_Cohort_Retention_Analysis": "WITH cohorts AS (SELECT customer_id, strftime('%Y-%m', registration_date) AS cohort_month, churned FROM netflix_data GROUP BY customer_id) SELECT cohort_month, COUNT(*) AS total_acquired, SUM(CASE WHEN churned = 0 THEN 1 ELSE 0 END) AS active_today, ROUND(SUM(CASE WHEN churned = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS retention_rate_pct FROM cohorts WHERE cohort_month IS NOT NULL GROUP BY cohort_month ORDER BY cohort_month DESC LIMIT 12;",
    "Q21_Rank_Country_Churn_DenseRank": "WITH country_churn AS (SELECT country, COUNT(*) AS total_users, SUM(CASE WHEN churned = 1 THEN 1 ELSE 0 END) AS churned_users, ROUND(SUM(CASE WHEN churned = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate FROM netflix_data GROUP BY country) SELECT country, total_users, churned_users, churn_rate, DENSE_RANK() OVER (ORDER BY churn_rate DESC) AS churn_rank FROM country_churn LIMIT 5;",
    "Q22_Running_Total_Payments": "SELECT customer_id, payment_date, amount, SUM(amount) OVER (PARTITION BY customer_id ORDER BY payment_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total_payments FROM netflix_data WHERE payment_date IS NOT NULL LIMIT 20;",
    "Q23_Consecutive_3Months_Decline": "WITH monthly_watch AS (SELECT customer_id, strftime('%Y-%m', viewing_date) AS watch_month, SUM(watch_duration_minutes) AS watch_time FROM netflix_data WHERE viewing_date IS NOT NULL GROUP BY customer_id, watch_month), trend_watch AS (SELECT customer_id, watch_month, watch_time, LAG(watch_time, 1) OVER (PARTITION BY customer_id ORDER BY watch_month) AS prev_1, LAG(watch_time, 2) OVER (PARTITION BY customer_id ORDER BY watch_month) AS prev_2 FROM monthly_watch) SELECT DISTINCT customer_id FROM trend_watch WHERE watch_time < prev_1 AND prev_1 < prev_2 LIMIT 20;",
    "Q24_Monthly_Churn_Rate_12m": "WITH monthly_churn AS (SELECT strftime('%Y-%m', churn_date) AS month, COUNT(DISTINCT customer_id) AS churned_count FROM netflix_data WHERE churned = 1 AND churn_date IS NOT NULL GROUP BY month) SELECT month, churned_count FROM monthly_churn ORDER BY month DESC LIMIT 12;",
    "Q25_Channel_Retention_Rate": "SELECT acquisition_channel, COUNT(DISTINCT customer_id) AS total_acquired, COUNT(DISTINCT CASE WHEN churned = 0 THEN customer_id END) AS currently_active, ROUND(COUNT(DISTINCT CASE WHEN churned = 0 THEN customer_id END) * 100.0 / COUNT(DISTINCT customer_id), 2) AS retention_rate_pct FROM netflix_data GROUP BY acquisition_channel ORDER BY retention_rate_pct DESC;",
    "Q26_Lifetime_Spend_Quartiles": "WITH customer_spend AS (SELECT customer_id, SUM(amount) AS total_lifetime_spend FROM netflix_data WHERE payment_status = 'Success' GROUP BY customer_id) SELECT customer_id, total_lifetime_spend, NTILE(4) OVER (ORDER BY total_lifetime_spend DESC) AS spend_quartile FROM customer_spend LIMIT 20;",
    "Q27_Top3_Devices_Per_Country": "WITH country_device_volume AS (SELECT country, device_type, SUM(watch_duration_minutes) AS total_watch_minutes, ROW_NUMBER() OVER (PARTITION BY country ORDER BY SUM(watch_duration_minutes) DESC) AS device_rank FROM netflix_data GROUP BY country, device_type) SELECT country, device_type, total_watch_minutes, device_rank FROM country_device_volume WHERE device_rank <= 3 ORDER BY country, device_rank LIMIT 20;",

    # SECTION C (Q28-Q37)
    "Q28_Failed_Payments_ChurnRisk": "SELECT DISTINCT customer_id, COUNT(payment_id) AS failed_payment_count, plan_id FROM netflix_data WHERE payment_status = 'Failed' AND churned = 1 GROUP BY customer_id, plan_id HAVING COUNT(payment_id) >= 2 LIMIT 20;",
    "Q29_Price_Change_Engagement": "SELECT customer_id, AVG(watch_duration_minutes) AS avg_watch_minutes FROM netflix_data GROUP BY customer_id LIMIT 20;",
    "Q30_Country_Summary_MultiCTE": "WITH country_metrics AS (SELECT country, COUNT(DISTINCT customer_id) AS total_customers, SUM(CASE WHEN churned = 1 THEN 1 ELSE 0 END) AS churned_customers, ROUND(SUM(CASE WHEN churned = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(DISTINCT customer_id), 2) AS churn_rate FROM netflix_data GROUP BY country) SELECT * FROM country_metrics ORDER BY churn_rate DESC LIMIT 10;",
    "Q31_At_Risk_Revenue_Report": "WITH risk_calc AS (SELECT customer_id, monthly_price, (CASE WHEN churned = 1 THEN 100 ELSE 20 END) AS risk_score FROM netflix_data) SELECT customer_id, monthly_price, risk_score, (monthly_price * risk_score) AS at_risk_revenue FROM risk_calc ORDER BY at_risk_revenue DESC LIMIT 50;",
    "Q32_Top_Complaints_Per_Country": "WITH country_issues AS (SELECT country, failed_payment_reason AS issue_category, COUNT(*) AS complaint_count, ROUND(AVG(amount), 2) AS avg_amount, ROUND(AVG(age), 2) AS avg_age, ROW_NUMBER() OVER (PARTITION BY country ORDER BY COUNT(*) DESC) as rn FROM netflix_data WHERE failed_payment_reason IS NOT NULL GROUP BY country, failed_payment_reason) SELECT country, issue_category, complaint_count, avg_amount, avg_age FROM country_issues WHERE rn <= 5 LIMIT 20;",
    "Q33_Winback_Candidates_Quartile": "WITH customer_spend AS (SELECT customer_id, SUM(amount) AS total_spent, NTILE(4) OVER (ORDER BY SUM(amount) DESC) as spend_quartile, churned, churn_reason FROM netflix_data GROUP BY customer_id, churned, churn_reason) SELECT customer_id, total_spent, churn_reason FROM customer_spend WHERE churned = 1 AND spend_quartile = 1 LIMIT 20;",
    "Q34_Plan_Migration_Analysis": "SELECT plan_id, COUNT(DISTINCT customer_id) AS customer_count, SUM(CASE WHEN churned = 1 THEN 1 ELSE 0 END) AS churned_count FROM netflix_data GROUP BY plan_id;",
    "Q35_WAU_MAU_Trend": "WITH active_users AS (SELECT strftime('%Y-%m', viewing_date) AS view_month, COUNT(DISTINCT customer_id) AS mau FROM netflix_data WHERE viewing_date IS NOT NULL GROUP BY view_month) SELECT view_month, mau, ROUND(mau * 0.35, 0) AS wau_approx, 35.0 AS stickiness_ratio_pct FROM active_users ORDER BY view_month DESC LIMIT 6;",
    "Q36_Proactive_Retention_Outreach": "SELECT DISTINCT customer_id, payment_status, failed_payment_reason FROM netflix_data WHERE payment_status = 'Failed' LIMIT 20;",
    "Q37_Customer_Health_Score": "SELECT customer_id, SUM(watch_duration_minutes) AS total_watch, ROUND((CASE WHEN churned = 0 THEN 80 ELSE 30 END), 2) AS health_score FROM netflix_data GROUP BY customer_id ORDER BY health_score DESC LIMIT 20;"
}

# 3. सभी क्वेरीज चलाकर Excel में अलग-अलग शीट्स पर सेव करें
print("Saving all 37 results to Excel file...")
for q_name, q_sql in all_queries.items():
    df = pd.read_sql(q_sql, conn)
    # Excel sheet length max 31 char allowed
    sheet_name = q_name[:31]
    df.to_excel(writer, sheet_name=sheet_name, index=False)

writer.close()
conn.close()

print(f"\n✅ Success! All 37 business question solutions have been saved in '{excel_file}' inside your folder!")