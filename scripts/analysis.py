import pandas as pd

# Load the CSV file
df = pd.read_csv('data/processed/Jobs_applied_public_processed.csv', parse_dates=['date applied'])


# Stats

# Number of jobs applied per year
year_applied = df.groupby("year_applied").size()
print(year_applied)

# Number of jobs applied per year and per month
month_applied = df.groupby(["year_applied", "month_applied"]).size()
print(month_applied)

# Number of jobs applied per month in 2024
rslt_df = df[df['year_applied']  == 2024]
# print(rslt_df) 
month_applied_2024 = df.groupby(["month_applied"]).size()
print(month_applied_2024)

# What do I want? 

# 	- % waiting for responses

# 	- Job titles applied
# 	- Job roles applied
# 	- Number of first interviews (%?)
# 	- Automated first interview (% of first interviews)
# 	- Percentage of those that make it to tech test? 
# 	- Types of tech test
#     - Percentage of those that get to final interview



# print(df)
# print(df[['role', 'date applied']].head(10))

# # Export to csv
# df.to_csv('data/processed/Jobs_applied_public_processed_test_analysis.csv')