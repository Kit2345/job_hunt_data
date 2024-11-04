import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 

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
ax.set_title('Figure 1: Number of applications by year')


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
ax.set_title('Figure 2: Number of applications by month in 2024')


# plt.show()



# % waiting for responses
received_reply = df.groupby('received_reply').size()
received_reply_df = received_reply.reset_index(name='count')
# print(received_reply)

colours = ["red", "green"]

fig, ax = plt.subplots()
ax.pie(received_reply_df["count"], labels=received_reply_df["received_reply"], autopct='%1.1f%%', startangle=90)
ax.set_title("Figure 3: Have I received a reply from the job I applied for?")
# plt.show()



# Number of first interviews (%?)
first_interviews = df.groupby("first").size()
first_interviews_df = first_interviews.reset_index(name="first_interview")




first_interviews_df.rename(columns={'first': 'status'}, inplace=True)
first_interviews_df = first_interviews_df[first_interviews_df['status'] != "speculative"] 


# first_interviews_df = rename_row(first_interviews_df, "status", "yes", "had_first_interview")
# first_interviews_df = rename_row(first_interviews_df, "status", "waiting", "waiting_on_cv_sieve")
# first_interviews_df = rename_row(first_interviews_df, "status", "no", "no_first_interview")
# first_interviews_df = rename_row(first_interviews_df, "status", "skip", "skipped_first_interview")

# print(first_interviews)
# print("first interviews:")
# print(first_interviews_df)

skip_value = first_interviews_df.loc[first_interviews_df['status'] == "skip", "first_interview"].sum()
yes_value = first_interviews_df.loc[first_interviews_df['status'] == "yes", "first_interview"].sum()

new_yes_value = skip_value + yes_value

first_interviews_df.loc[first_interviews_df['status'] == "yes", "first_interview"] = new_yes_value

# print("test found")
# print(skip_value)
# print(yes_value)
# print(new_yes_value)

first_interviews_df.loc[first_interviews_df['status'] == "yes", "first_interview"] = new_yes_value
first_interviews_df = first_interviews_df[first_interviews_df['status'] != "skip"] 

print("first interviews:")
print(first_interviews_df)






# Percentage of those that make it to tech test? 
rslt_df = df[(df['first']  == "yes") | (df['first']  == "skip")]
to_tech_test = rslt_df.groupby("tech").size()
to_tech_test_df = to_tech_test.reset_index(name="tech_test")

to_tech_test_df.rename(columns={'tech': 'status'}, inplace=True)

# to_tech_test_df = rename_row(to_tech_test_df, "status", "no", "rejected_at_first_interview")
# to_tech_test_df = rename_row(to_tech_test_df, "status", "waiting", "waiting_on_first_interview")
# to_tech_test_df = rename_row(to_tech_test_df, "status", "yes", "took_tech_test")



print("tech test:")
print(to_tech_test_df)




# Percentage of those that get to final interview
rslt_df = df[df['tech']  == "yes"]
to_final = rslt_df.groupby("final").size()
to_final_df = to_final.reset_index(name="final_interview")

to_final_df.rename(columns={'final': 'status'}, inplace=True)
# to_final_df = rename_row(to_final_df, "status", "yes", "had_final_interview")
# to_final_df = rename_row(to_final_df, "status", "no", "rejected_at_tech_test")

# print(to_final)
print("final")
print(to_final_df)


# summary_df = pd.concat([first_interviews_df, to_tech_test_df, to_final_df], ignore_index=True)




summary_df = pd.merge(first_interviews_df, to_tech_test_df, on='status', how='outer').fillna(0)
summary_df = pd.merge(summary_df, to_final_df, on='status', how='outer').fillna(0)
print("summary")
print(summary_df)

# Create stacked bar graph 

summary_df = summary_df.reindex([2, 1, 0])
print(summary_df)

yes_status = summary_df.loc[summary_df['status'] == "yes", ["first_interview", "tech_test", "final_interview"]].values[0].tolist()

waiting_status = summary_df.loc[summary_df['status'] == "waiting", ["first_interview", "tech_test", "final_interview"]].values[0].tolist()

no_status = summary_df.loc[summary_df['status'] == "no", ["first_interview", "tech_test", "final_interview"]].values[0].tolist()

print(yes_status)
print(waiting_status)
print(no_status)

stage = (
    "applied",
    "first_interview",
    "tech_test",
    
)
status = {
    "passed": np.array(yes_status),
    "waiting": np.array(waiting_status),
    "rejected": np.array(no_status),
}

colors = {
    "passed": "tab:green",
    "waiting": "tab:blue",
    "rejected": "tab:red",
}

width = 0.5



fig, ax = plt.subplots()
bottom = np.zeros(3)

for boolean, current_status in status.items():
    p = ax.bar(stage, current_status, width, label=boolean, bottom=bottom, color = colors[boolean])
    

    # Add the labels centered in the bars
    for i, value in enumerate(current_status):
        if value > 0:  # Only label if the value is greater than zero
            ax.text(p[i].get_x() + p[i].get_width() / 2,  # X position
                    bottom[i] + value / 2,  # Y position, centered in the bar
                    value,  # Label from the dictionary
                    ha='center', va='center', color='black', fontsize=8)  # Center the text and set color

    bottom += current_status

ax.set_title("Figure 4: Summary of the status of the jobs I applied for")
ax.legend(loc="upper right")

# plt.show()


# Percentage stacked plot 

totals = summary_df[['first_interview', 'tech_test', 'final_interview']].sum()
print("totals")
print(totals)

percentage_df = summary_df.copy()  
percentage_df[['first_interview', 'tech_test', 'final_interview']] = (
    summary_df[['first_interview', 'tech_test', 'final_interview']].div(totals) * 100
).round(1)

print(percentage_df)

yes_status_percentage = percentage_df.loc[percentage_df['status'] == "yes", ["first_interview", "tech_test", "final_interview"]].values[0].tolist()

waiting_status_percentage = percentage_df.loc[percentage_df['status'] == "waiting", ["first_interview", "tech_test", "final_interview"]].values[0].tolist()

no_status_percentage = percentage_df.loc[percentage_df['status'] == "no", ["first_interview", "tech_test", "final_interview"]].values[0].tolist()

status_percentage = {
    "passed": np.array(yes_status_percentage),
    "waiting": np.array(waiting_status_percentage),
    "rejected": np.array(no_status_percentage),
}


fig, ax = plt.subplots()
bottom = np.zeros(3)

for boolean, current_status in status_percentage.items():
    p = ax.bar(stage, current_status, width, label=boolean, bottom=bottom, color = colors[boolean])
    

    # Add the labels centered in the bars
    for i, value in enumerate(current_status):
        if value > 0:  # Only label if the value is greater than zero
            ax.text(p[i].get_x() + p[i].get_width() / 2,  # X position
                    bottom[i] + value / 2,  # Y position, centered in the bar
                    f"{value}%",  # Label from the dictionary
                    ha='center', va='center', color='black', fontsize=8)  # Center the text and set color

    bottom += current_status

ax.set_title("Figure 5: Summary of the status of the jobs I applied for")
ax.legend(loc="upper right")

# plt.show()



# Automated first interview (% of first interviews)

# Select for first interviews
rslt_df = df[df['first']  == "yes"]
# print(rslt_df[["first", "tech", "automated first?"]])

# Separate automated and not automated into separate items
automated_first_interview = rslt_df.loc[rslt_df["automated first?"] == "yes"]
not_automated_first_interview = rslt_df.loc[rslt_df["automated first?"] == "no"]
# print("automated")
# print(automated_first_interview[["first", "tech", "automated first?"]])
# print("not automated")
# print(not_automated_first_interview[["first", "tech", "automated first?"]])

# Summarise the automated and not automated applications
automated_first_interview = automated_first_interview.groupby("tech").size()
not_automated_first_interview = not_automated_first_interview.groupby("tech").size()
# print("automated")
# print(automated_first_interview)
# print("not automated")
# print(not_automated_first_interview)

# Change the automated and not automated applications into dataframes
automated_first_interview_df = automated_first_interview.reset_index(name="automated")
automated_first_interview_df.rename(columns={'tech': 'status'}, inplace=True)
# print(automated_first_interview_df)
not_automated_first_interview_df = not_automated_first_interview.reset_index(name="not_automated")
not_automated_first_interview_df.rename(columns={'tech': 'status'}, inplace=True)
# print(not_automated_first_interview_df)

# Merge the two summary  tables together
automation_summary_df =pd.merge(automated_first_interview_df, not_automated_first_interview_df, on="status", how="outer").fillna(0)
print("automation summary")
print(automation_summary_df)

# Stacked bar graph 

# Re-order rows so it is yes waiting no
automation_summary_df = automation_summary_df.reindex([2, 1, 0])
print(automation_summary_df)

# Getting each status into new python list 
yes_status = automation_summary_df.loc[automation_summary_df['status'] == "yes", ["automated", "not_automated"]].values[0].tolist()
waiting_status = automation_summary_df.loc[automation_summary_df['status'] == "waiting", ["automated", "not_automated"]].values[0].tolist()
no_status = automation_summary_df.loc[automation_summary_df['status'] == "no", ["automated", "not_automated"]].values[0].tolist()
print(yes_status)
print(waiting_status)
print(no_status)

# Define variables to use for plot
stage = (
    "automated",
    "not_automated",
)

status = {
    "passed": np.array(yes_status),
    "waiting": np.array(waiting_status),
    "rejected": np.array(no_status),
}

colors = {
    "passed": "tab:green",
    "waiting": "tab:blue",
    "rejected": "tab:red",
}

width = 0.5

# Draw plot
fig, ax = plt.subplots()
bottom = np.zeros(2)

for boolean, current_status in status.items():
    p = ax.bar(stage, current_status, width, label=boolean, bottom=bottom, color = colors[boolean])
    

    # Add the labels centered in the bars
    for i, value in enumerate(current_status):
        if value > 0:  # Only label if the value is greater than zero
            ax.text(p[i].get_x() + p[i].get_width() / 2,  # X position
                    bottom[i] + value / 2,  # Y position, centered in the bar
                    round(value),  # Label from the dictionary
                    ha='center', va='center', color='black', fontsize=8)  # Center the text and set color

    bottom += current_status

ax.set_title("Figure 6: Comparing status of automated and not automated first interviews")
ax.legend(loc="upper center")

# plt.show()


# Automation Percentage Stacked Bar Graph 

# Getting totals 
automation_totals = automation_summary_df[["automated", "not_automated"]].sum()
print("totals")
print(automation_totals)


automation_percentage_df = automation_summary_df.copy()  
automation_percentage_df[["automated", "not_automated"]] = (
    automation_percentage_df[["automated", "not_automated"]].div(automation_totals) * 100
).round(1)

print(automation_percentage_df)

# Getting status into python list
yes_status_percentage = automation_percentage_df.loc[automation_percentage_df['status'] == "yes", ["automated", "not_automated"]].values[0].tolist()
waiting_status_percentage = automation_percentage_df.loc[automation_percentage_df['status'] == "waiting", ["automated", "not_automated"]].values[0].tolist()
no_status_percentage = automation_percentage_df.loc[automation_percentage_df['status'] == "no", ["automated", "not_automated"]].values[0].tolist()
# print(yes_status_percentage)
# print(waiting_status_percentage)
# print(no_status_percentage)

status_percentage = {
    "passed": np.array(yes_status_percentage),
    "waiting": np.array(waiting_status_percentage),
    "rejected": np.array(no_status_percentage),
}

fig, ax = plt.subplots()
bottom = np.zeros(2)

for boolean, current_status in status_percentage.items():
    p = ax.bar(stage, current_status, width, label=boolean, bottom=bottom, color = colors[boolean])
    

    # Add the labels centered in the bars
    for i, value in enumerate(current_status):
        if value > 0:  # Only label if the value is greater than zero
            ax.text(p[i].get_x() + p[i].get_width() / 2,  # X position
                    bottom[i] + value / 2,  # Y position, centered in the bar
                    f"{value}%",  # Label from the dictionary
                    ha='center', va='center', color='black', fontsize=8)  # Center the text and set color

    bottom += current_status

ax.set_title("Figure 7: Comparing status of automated and not automated first interviews")
ax.legend(loc="upper center")

# plt.show()



# Types of tech tests

# Separate types of tech tests
rslt_df = df[df['tech']  == "yes"]
algo = rslt_df[rslt_df["tech test type"] == "algorithmic problems"]
pair_prog = rslt_df[rslt_df["tech test type"] == "Pair programming"]
take_home = rslt_df[rslt_df["tech test type"] == "take-home"]
# print(rslt_df["tech test type"])
# print(algo[["first", "tech", "final", "tech test type"]])
# print(pair_prog)
# print(take_home)

# Summarise status of different tech tests
algo_status = algo.groupby("final").size()
pair_prog_status =  pair_prog.groupby("final").size()
take_home_status = take_home.groupby("final").size()
# print(algo_status)
# print(pair_prog_status)
# print(take_home_status)

# Change the tech test status into dataframes
algo_status_df = algo_status.reset_index(name="algo")
algo_status_df.rename(columns={'final': 'status'}, inplace=True)
# print(algo_status_df)
pair_prog_status_df = pair_prog_status.reset_index(name="pair_prog")
pair_prog_status_df.rename(columns={'final': 'status'}, inplace=True)
# print(pair_prog_status_df)
take_home_status_df = take_home_status.reset_index(name="take_home")
take_home_status_df.rename(columns={'final': 'status'}, inplace=True)
# print(take_home_status_df)



# # Merge the two summary  tables together
tech_test_summary_df = pd.merge(algo_status_df, pair_prog_status_df, on="status", how="outer").fillna(0)
# print(tech_test_summary_df)
tech_test_summary_df = pd.merge(tech_test_summary_df, take_home_status_df, on="status", how="outer").fillna(0)
# print(tech_test_summary_df)



# Re-order rows so it is yes waiting no
tech_test_summary_df = tech_test_summary_df.reindex([1, 0])
print(tech_test_summary_df)

# Getting each status into new python list 
yes_status = tech_test_summary_df.loc[tech_test_summary_df['status'] == "yes", ["algo", "pair_prog", "take_home"]].values[0].tolist()
# waiting_status = tech_test_summary_df.loc[tech_test_summary_df['status'] == "waiting", ["algo", "pair_prog", "take_home"]].values[0].tolist()
no_status = tech_test_summary_df.loc[tech_test_summary_df['status'] == "no", ["algo", "pair_prog", "take_home"]].values[0].tolist()
# print(yes_status)
# print(waiting_status)
# print(no_status)

# Define variables to use for plot
stage = (
    "algorithmic_problems",
    "pair_progamming",
    "take_home"
)

status = {
    "passed": np.array(yes_status),
    # "waiting": np.array(waiting_status),
    "rejected": np.array(no_status),
}

colors = {
    "passed": "tab:green",
    # "waiting": "tab:blue",
    "rejected": "tab:red",
}

width = 0.5

# # Draw plot
fig, ax = plt.subplots()
bottom = np.zeros(3)

for boolean, current_status in status.items():
    p = ax.bar(stage, current_status, width, label=boolean, bottom=bottom, color = colors[boolean])
    

    # Add the labels centered in the bars
    for i, value in enumerate(current_status):
        if value > 0:  # Only label if the value is greater than zero
            ax.text(p[i].get_x() + p[i].get_width() / 2,  # X position
                    bottom[i] + value / 2,  # Y position, centered in the bar
                    round(value),  # Label from the dictionary
                    ha='center', va='center', color='black', fontsize=8)  # Center the text and set color

    bottom += current_status

ax.set_title("Figure 8: Comparing status of different types of tech tests")
ax.legend(loc="upper right")
# plt.show()

# Tech test Percentage Stacked Bar Graph 

# Getting totals 
tech_test_totals = tech_test_summary_df[["algo", "pair_prog", "take_home"]].sum()
print("totals")
# print(tech_test_totals)


tech_test_percentage_df = tech_test_summary_df.copy()  
tech_test_percentage_df[["algo", "pair_prog", "take_home"]] = (
    tech_test_percentage_df[["algo", "pair_prog", "take_home"]].div(tech_test_totals) * 100
).round(1)

# print(tech_test_percentage_df)

# Getting status into python list
yes_status_percentage = tech_test_percentage_df.loc[tech_test_percentage_df['status'] == "yes", ["algo", "pair_prog", "take_home"]].values[0].tolist()
# yes_status_percentage = tech_test_percentage_df.loc[tech_test_percentage_df['status'] == "waiting", ["algo", "pair_prog", "take_home"]].values[0].tolist()
no_status_percentage = tech_test_percentage_df.loc[tech_test_percentage_df['status'] == "no", ["algo", "pair_prog", "take_home"]].values[0].tolist()
# print(yes_status_percentage)
# print(waiting_status_percentage)
# print(no_status_percentage)

status_percentage = {
    "passed": np.array(yes_status_percentage),
    # "waiting": np.array(waiting_status_percentage),
    "rejected": np.array(no_status_percentage),
}

fig, ax = plt.subplots()
bottom = np.zeros(3)

for boolean, current_status in status_percentage.items():
    p = ax.bar(stage, current_status, width, label=boolean, bottom=bottom, color = colors[boolean])
    

    # Add the labels centered in the bars
    for i, value in enumerate(current_status):
        if value > 0:  # Only label if the value is greater than zero
            ax.text(p[i].get_x() + p[i].get_width() / 2,  # X position
                    bottom[i] + value / 2,  # Y position, centered in the bar
                    f"{value}%",  # Label from the dictionary
                    ha='center', va='center', color='black', fontsize=8)  # Center the text and set color

    bottom += current_status

ax.set_title("Figure 9: Comparing status of different types of tech test")
ax.legend(loc="upper right")

plt.show()





# What do I want? 

# 	- Job titles applied
# 	- Job roles applied
# 	- Types of tech test




# print(df)
# print(df[['role', 'date applied']].head(10))

# # Export to csv
# df.to_csv('data/processed/Jobs_applied_public_processed_test_analysis.csv')