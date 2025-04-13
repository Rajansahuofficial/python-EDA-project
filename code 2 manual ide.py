import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style and figure size for all plots
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)

# Load and clean the dataset
print("Loading dataset...")
df = pd.read_excel("Crime_Data_from_2020_to_Present python prjt.xlsx")

# Clean column names (remove spaces, make uppercase)
df.columns = df.columns.str.strip().str.upper().str.replace(" ", "_")

# Convert date columns to proper datetime
df['DATE_OCC'] = pd.to_datetime(df['DATE_OCC'], errors='coerce')
df['DATE_RPTD'] = pd.to_datetime(df['DATE_RPTD'], errors='coerce')

# Convert TIME_OCC to string and extract hour
df['TIME_OCC'] = df['TIME_OCC'].astype(str).str.zfill(4)
df['HOUR'] = df['TIME_OCC'].str[:2].astype(int)

# Extract year and month from DATE_OCC
df['YEAR'] = df['DATE_OCC'].dt.year
df['MONTH'] = df['DATE_OCC'].dt.month

# Drop rows without location (latitude and longitude)
df = df.dropna(subset=['LAT', 'LON'])

# Save cleaned data (optional)
df.to_excel("Cleaned_Crime_Data.xlsx", index=False)

print("\nDataset Information:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nFirst 5 Rows:")
print(df.head())

correlation = df.corr(numeric_only=True)

plt.figure()
sns.heatmap(correlation, annot=True, cmap="Blues")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.show()


crime_by_month = df.groupby(['YEAR', 'MONTH']).size().reset_index(name='INCIDENTS')
crime_by_month['DATE'] = pd.to_datetime(crime_by_month[['YEAR', 'MONTH']].assign(DAY=1))

plt.figure()
sns.lineplot(data=crime_by_month, x='DATE', y='INCIDENTS')
plt.title("Crime Incidents Over Time")
plt.xlabel("Date")
plt.ylabel("Number of Crimes")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


plt.figure()
sns.histplot(df['HOUR'], bins=24, kde=True)
plt.title("Crimes by Hour of Day")
plt.xlabel("Hour")
plt.ylabel("Number of Crimes")
plt.tight_layout()
plt.show()


heat_data = df.groupby(['YEAR', 'MONTH']).size().unstack(fill_value=0)

plt.figure()
sns.heatmap(heat_data, cmap="Reds")
plt.title("Seasonal Crime Heatmap")
plt.tight_layout()
plt.show()


# TOP 10 HIGH-CRIME AREAS

top_areas = df['AREA_NAME'].value_counts().head(10)

plt.figure()
sns.barplot(x=top_areas.values, y=top_areas.index)
plt.title("Top 10 Crime Areas")
plt.xlabel("Number of Crimes")
plt.tight_layout()
plt.show()

# TOP 10 CRIME TYPES

top_crimes = df['CRM_CD_DESC'].value_counts().head(10)

plt.figure()
sns.barplot(x=top_crimes.values, y=top_crimes.index)
plt.title("Top 10 Crime Types")
plt.xlabel("Frequency")
plt.tight_layout()
plt.show()

# ========================
# TOP 10 WEAPONS USED
# ========================
weapon_usage = df['WEAPON_DESC'].value_counts().head(10)

plt.figure()
sns.barplot(x=weapon_usage.values, y=weapon_usage.index)
plt.title("Top 10 Weapons Used")
plt.xlabel("Frequency")
plt.tight_layout()
plt.show()

# VICTIM AGE DISTRIBUTION
plt.figure()
sns.histplot(df['VICT_AGE'].dropna(), bins=20, kde=True, color='purple')
plt.title("Victim Age Distribution")
plt.xlabel("Age")
plt.ylabel("Number of Victims")
plt.tight_layout()
plt.show()

# GENDER DISTRIBUTION
gender = df['VICT_SEX'].value_counts()

plt.figure()
sns.barplot(x=gender.index, y=gender.values)
plt.title("Gender Distribution of Victims")
plt.xlabel("Gender")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# ETHNICITY DISTRIBUTION
ethnicity = df['VICT_DESCENT'].value_counts().head(10)

plt.figure()
sns.barplot(x=ethnicity.values, y=ethnicity.index)
plt.title("Top Ethnic Groups Affected")
plt.xlabel("Number of Victims")
plt.tight_layout()
plt.show()

# CRIME RESOLUTION STATUS
status = df['STATUS_DESC'].value_counts()

plt.figure()
plt.pie(status, labels=status.index, autopct='%1.1f%%', startangle=140)
plt.title("Crime Resolution Status")
plt.tight_layout()
plt.show()

# Stacked bar chart for resolution by top crime types
top_types = df['CRM_CD_DESC'].value_counts().nlargest(5).index
status_by_type = df[df['CRM_CD_DESC'].isin(top_types)].groupby(['CRM_CD_DESC', 'STATUS_DESC']).size().unstack().fillna(0)

status_by_type.plot(kind='bar', stacked=True, colormap='Set2', figsize=(10, 6))
plt.title("Resolution Status for Top 5 Crime Types")
plt.xlabel("Crime Type")
plt.ylabel("Number of Cases")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
