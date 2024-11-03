import pandas as pd
import matplotlib.pyplot as plt

def rename_row(name_df, column_name, current_name, new_name):
    name_df.loc[name_df[column_name] == current_name, column_name] = new_name
    return name_df


# Load the CSV file
df = pd.read_csv('data/processed/Jobs_applied_public_processed.csv', parse_dates=['date applied'])


# Stats

# Number of jobs applied per year
year_applied = df.groupby("year_applied").size()
year_applied_df = year_applied.reset_index(name='count')

# print(year_applied)
# print(year_applied_df)

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
# print(month_applied_2024)
# print(month_applied_2024_df)


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
# print(received_reply)

colours = ["red", "green"]

fig, ax = plt.subplots()
ax.pie(received_reply_df["count"], labels=received_reply_df["received_reply"], autopct='%1.1f%%', startangle=90)
ax.set_title("Have I received a reply from the job I applied for?")
# plt.show()



# Number of first interviews (%?)
first_interviews = df.groupby("first").size()
first_interviews_df = first_interviews.reset_index(name="count")



# first_interviews_df.rename(columns={'first': 'status'}, inplace=True)
first_interviews_df = first_interviews_df[first_interviews_df['status'] != "speculative"] 

# first_interviews_df = rename_row(first_interviews_df, "status", "yes", "had_first_interview")
# first_interviews_df = rename_row(first_interviews_df, "status", "waiting", "waiting_on_cv_sieve")
# first_interviews_df = rename_row(first_interviews_df, "status", "no", "no_first_interview")
# first_interviews_df = rename_row(first_interviews_df, "status", "skip", "skipped_first_interview")

# print(first_interviews)
print("first interviews:")
print(first_interviews_df)


# def rename_row(name_df, column_name, current_name, new_name):
#     name_df[name_df[column_name] == current_name, current_name] = new_name



# # Automated first interview (% of first interviews)
# rslt_df = df[df['first']  == "yes"]
# automated_first_interview = rslt_df.groupby("automated first?").size()
# automated_first_interview_df = automated_first_interview.reset_index(name="count")
# # print(rslt_df[["number", "role", "first"]])
# # print(automated_first_interview)
# print("automated first interview?:")
# print(automated_first_interview_df)



# Percentage of those that make it to tech test? 
rslt_df = df[(df['first']  == "yes") | (df['first']  == "skip")]
to_tech_test = rslt_df.groupby("tech").size()
to_tech_test_df = to_tech_test.reset_index(name="count")

# to_tech_test_df.rename(columns={'tech': 'status'}, inplace=True)

# to_tech_test_df = rename_row(to_tech_test_df, "status", "no", "rejected_at_first_interview")
# to_tech_test_df = rename_row(to_tech_test_df, "status", "waiting", "waiting_on_first_interview")
# to_tech_test_df = rename_row(to_tech_test_df, "status", "yes", "took_tech_test")



print("tech test:")
print(to_tech_test_df)




# Percentage of those that get to final interview
rslt_df = df[df['tech']  == "yes"]
to_final = rslt_df.groupby("final").size()
to_final_df = to_final.reset_index(name="count")

# to_final_df.rename(columns={'final': 'status'}, inplace=True)
# to_final_df = rename_row(to_final_df, "status", "yes", "had_final_interview")
# to_final_df = rename_row(to_final_df, "status", "no", "rejected_at_tech_test")

print(to_final)
print(to_final_df)


# summary_df = pd.concat([first_interviews_df, to_tech_test_df, to_final_df], ignore_index=True)

# print(summary_df)





# What do I want? 

# 	- Job titles applied
# 	- Job roles applied
# 	- Types of tech test
#     - Percentage of those that get to final interview



# print(df)
# print(df[['role', 'date applied']].head(10))

# # Export to csv
# df.to_csv('data/processed/Jobs_applied_public_processed_test_analysis.csv')