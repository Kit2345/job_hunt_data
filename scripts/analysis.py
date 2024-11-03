import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv('data/processed/Jobs_applied_public_processed.csv', parse_dates=['date applied'])


# Stats

# Number of jobs applied per year
year_applied = df.groupby("year_applied").size()
year_applied_df = year_applied.reset_index(name='count')

print(year_applied)
print(year_applied_df)




fig, ax = plt.subplots()

ax.bar(year_applied_df["year_applied"], year_applied_df["count"]) 

ax.set_xticks(year_applied_df["year_applied"])

ax.set_ylabel('Number of applications')
ax.set_xlabel('Year')
ax.set_title('Number of applications by year')


# plt.show()



# # Number of jobs applied per year and per month
# month_applied = df.groupby(["year_applied", "month_applied"]).size()
# print(month_applied)

# Number of jobs applied per month in 2024
rslt_df = df[df['year_applied']  == 2024]
# print(rslt_df) 
month_applied_2024 = rslt_df.groupby(["month_applied"]).size()
month_applied_2024_df = month_applied_2024.reset_index(name='count')
print(month_applied_2024)
print(month_applied_2024_df)


fig, ax = plt.subplots()

ax.bar(month_applied_2024_df["month_applied"], month_applied_2024_df["count"]) 

ax.set_xticks(month_applied_2024_df["month_applied"])

ax.set_ylabel('Number of applications')
ax.set_xlabel('Month')
ax.set_title('Number of applications by month in 2024')


# plt.show()



# % waiting for responses
received_reply = df.groupby('received_reply').size()
received_reply_df = received_reply.reset_index(name='count')
print(received_reply)

colours = ["red", "green"]

fig, ax = plt.subplots()
ax.pie(received_reply_df["count"], labels=received_reply_df["received_reply"], autopct='%1.1f%%', startangle=90)
plt.show()



# # Number of first interviews (%?)
# first_interviews = df.groupby("first").size()
# print(first_interviews)

# # Automated first interview (% of first interviews)
# rslt_df = df[df['first']  == "yes"]
# automated_first_interview = rslt_df.groupby("automated first?").size()
# # print(rslt_df[["number", "role", "first"]])
# print(automated_first_interview)

# # Percentage of those that make it to tech test? 
# rslt_df = df[df['first']  == "yes"]
# to_tech_test = rslt_df.groupby("tech").size()
# print(to_tech_test)






# What do I want? 

# 	- Job titles applied
# 	- Job roles applied
# 	- Types of tech test
#     - Percentage of those that get to final interview



# print(df)
# print(df[['role', 'date applied']].head(10))

# # Export to csv
# df.to_csv('data/processed/Jobs_applied_public_processed_test_analysis.csv')