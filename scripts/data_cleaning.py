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
        return "intern"
    elif "apprenticeship" in role: 
        return "apprentice"
    elif "graduate" in role: 
        return "graduate"
    elif "academy" in role or "training" in role or "trainee" in role:
        return "trainee"
    elif "speculative" in role:
        return "speculative"
    elif "associate" in role or "junior" in role or "software engineer i" in role or "entry-level" in role:
        return "junior"
    else:
        return "mid"

df['job_title'] = df['role'].apply(categorize_job_title)

# New column: job_role
def catergorize_job_role(role):
    role = role.lower()

    if "speculative" in role: 
        return "speculative"
    elif "support" in role: 
        return "support"
    elif "mobile" in role or "react native" in role:
        return "mobile developer"
    elif "frontend" in role or "front-end" in role or "front end" in role:
        return "front-end"
    elif "backend" in role or "back-end" in role or "back end" in role:
        return "back-end"
    elif "fullstack" in role or "full-stack" in role or "full stack" in role:
        return "full stack"
    elif "web developer" in role:
        return "web developer"
    elif "data engineer" in role:
        return "data engineer"
    elif "data analyst" in role:
        return "data analyst"
    elif "qa" in role or "test" in role:
        return "qa engineer"
    elif "product engineer" in role:
        return "product engineer"
    else:
        return "software engineer"

df["job_role"] = df["role"].apply(catergorize_job_role)


print(df)
print(df[['role']].head(10))


#Export to csv
df.to_csv('data/processed/Jobs_applied_public_processed.csv')

