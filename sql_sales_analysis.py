import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# 1) Load a stable dataset (same one you already used)
url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"
df = pd.read_csv(url)

# 2) Create an in-memory SQLite database (no installs needed)
conn = sqlite3.connect(":memory:")

# 3) Write the dataframe to a SQL table
df.to_sql("tips", conn, index=False, if_exists="replace")

# Helper to run SQL and return a dataframe
def q(sql: str) -> pd.DataFrame:
    return pd.read_sql_query(sql, conn)

print("=== Row count ===")
print(q("SELECT COUNT(*) AS row_count FROM tips;"))

print("\n=== Total revenue (sum of total_bill) ===")
print(q("SELECT ROUND(SUM(total_bill), 2) AS total_revenue FROM tips;"))

print("\n=== Average tip by day ===")
avg_tip_by_day = q("""
SELECT day,
       ROUND(AVG(tip), 3) AS avg_tip
FROM tips
GROUP BY day
ORDER BY avg_tip DESC;
""")
print(avg_tip_by_day)

print("\n=== Revenue by day ===")
revenue_by_day = q("""
SELECT day,
       ROUND(SUM(total_bill), 2) AS revenue
FROM tips
GROUP BY day
ORDER BY revenue DESC;
""")
print(revenue_by_day)

print("\n=== Top 5 bills (largest checks) ===")
print(q("""
SELECT total_bill, tip, sex, smoker, day, time, size
FROM tips
ORDER BY total_bill DESC
LIMIT 5;
"""))

print("\n=== Tip % by day (avg tip/avg bill) ===")
tip_pct_by_day = q("""
SELECT day,
       ROUND(AVG(tip) / AVG(total_bill) * 100, 2) AS avg_tip_pct
FROM tips
GROUP BY day
ORDER BY avg_tip_pct DESC;
""")
print(tip_pct_by_day)

# 4) Simple chart: Revenue by day
plt.bar(revenue_by_day["day"], revenue_by_day["revenue"])
plt.title("Revenue by Day (SQL Aggregation)")
plt.xlabel("Day")
plt.ylabel("Revenue")
plt.show()

conn.close()