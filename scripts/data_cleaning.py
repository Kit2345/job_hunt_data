import pandas as pd

# Load the CSV file
df = pd.read_csv('data/raw/Jobs_applied_public.csv')

# remove space in column names and make all lower case
df.rename(columns=lambda x: x.strip().lower(), inplace=True)

# Drop Company column
df.drop(columns=['company'],inplace=True)

# Delete rows with no information
df.dropna(subset=['role'], inplace=True)

# New column: job_title
def categorize_job_title(role): 
    role = role.lower()

    if "internship" in role:
        return "internship"
    elif "apprenticeship" in role: 
        return "apprenticeship"
    elif "graduate" in role: 
        return "graduate"
    elif "academy" in role or "training" in role or "trainee" in role:
        return "training programme"
    elif "speculative" in role:
        return "speculative"
    elif "associate" in role or "junior" in role or "software engineer i" in role or "entry-level" in role:
        return "junior"
    else:
        return "mid"

df['job_title'] = df['role'].apply(categorize_job_title)




print(df)
print(df[['role']].head(10))


#Export to csv
df.to_csv('data/processed/Jobs_applied_public_processed.csv')

