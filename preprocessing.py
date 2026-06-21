# ============================================================
# POPULATION DATA CLEANING & PREPROCESSING SCRIPT (FINAL FIXED)
# ============================================================

import pandas as pd

# ============================================================
# STEP 1: LOAD DATASET
# ============================================================

file_path = r"E:\Masters\UE\Data Analytics\Final submission\API_SP.POP.TOTL_DS2_en_csv_v2_406129\Updated_Main.csv"

df = pd.read_csv(file_path, engine='python', on_bad_lines='skip')

print("Initial Shape:", df.shape)


# ============================================================
# STEP 2: CONVERT WIDE → LONG (KEEP CONTINENT)
# ============================================================

# Remove unnecessary columns if present
cols_to_drop = ['Country Code', 'Indicator Name', 'Indicator Code']
df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])

# ✅ IMPORTANT: keep Continent also
id_columns = ['Country Name']

if 'Continent' in df.columns:
    id_columns.append('Continent')

df = df.melt(
    id_vars=id_columns,
    var_name='Year',
    value_name='Population'
)

# Rename column
df.rename(columns={'Country Name': 'Country'}, inplace=True)

print(df.head())


# ============================================================
# STEP 3: HANDLE MISSING VALUES
# ============================================================

print("\nMissing Values Before:\n", df.isnull().sum())

df['Population'] = df['Population'].astype(str).str.replace(',', '')
df['Population'] = pd.to_numeric(df['Population'], errors='coerce')

df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

df = df.dropna(subset=['Country', 'Year', 'Population'])

print("\nMissing Values After:\n", df.isnull().sum())


# ============================================================
# STEP 4: REMOVE DUPLICATES
# ============================================================

print("\nDuplicate Rows:", df.duplicated().sum())
df = df.drop_duplicates()


# ============================================================
# STEP 5: FIX FORMATTING ISSUES
# ============================================================

df['Country'] = df['Country'].str.strip()
df['Country'] = df['Country'].str.title()

df['Country'] = df['Country'].replace({
    'Usa': 'United States',
    'Uk': 'United Kingdom',
    'Uae': 'United Arab Emirates'
})


# ============================================================
# STEP 6: CONVERT DATA TYPES
# ============================================================

df['Year'] = df['Year'].astype(int)
df['Population'] = df['Population'].astype(float)


# ============================================================
# STEP 7: SORT DATA
# ============================================================

df = df.sort_values(by=['Country', 'Year'])


# ============================================================
# STEP 8: CREATE NEW COLUMNS
# ============================================================

df['Annual Change'] = df.groupby('Country')['Population'].diff()

df['Growth Rate (%)'] = df.groupby('Country')['Population'].pct_change() * 100

df['Decade'] = (df['Year'] // 10) * 10


def categorize_growth(rate):
    if pd.isna(rate):
        return "No Data"
    elif rate < 0:
        return "Negative"
    elif rate < 1:
        return "Low"
    elif rate < 2:
        return "Medium"
    else:
        return "High"


df['Growth Category'] = df['Growth Rate (%)'].apply(categorize_growth)


# ============================================================
# STEP 9: FINAL CHECK
# ============================================================

print("\nFinal Dataset Info:")
print(df.info())

print("\nSummary Statistics:")
print(df.describe())


# ============================================================
# STEP 10: SAVE CLEANED DATASET
# ============================================================

output_path = r"E:\Masters\UE\Data Analytics\Final submission\Cleaned_Population_Data.csv"
df.to_csv(output_path, index=False)

print("\nCleaned dataset saved as:", output_path)

# ============================================================
# END
# ============================================================