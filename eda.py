# ============================================================
# FINAL EDA SCRIPT (WITH TABLES + PLOTS IN PDF)
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns

# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(r"E:\Masters\UE\Data Analytics\Final submission\API_SP.POP.TOTL_DS2_en_csv_v2_406129\Cleaned_Population_Data.csv")

pdf = PdfPages("EDA_Analysis_Report.pdf")


# ============================================================
# FUNCTION TO SAVE TABLE AS PDF PAGE
# ============================================================

def save_table(df_table, title):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=df_table.values,
                     colLabels=df_table.columns,
                     loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(df_table.columns))))
    plt.title(title)
    pdf.savefig()
    plt.close()


# ============================================================
# PART 1: BASIC ANALYSIS
# ============================================================

# Total Population Plot
total_pop_year = df.groupby('Year')['Population'].sum()

plt.figure()
total_pop_year.plot()
plt.title("Total Population Over Time")
plt.xlabel("Year")
plt.ylabel("Population")
pdf.savefig()
plt.close()

# ------------------------------------------------------------
# TOP 10 COUNTRIES POPULATION TREND (WITH YEAR)
# ------------------------------------------------------------

# Get top 10 countries based on latest population
latest_year = df['Year'].max()

top10_countries = df[df['Year'] == latest_year] \
    .sort_values(by='Population', ascending=False) \
    .head(10)['Country']

df_top10 = df[df['Country'].isin(top10_countries)]

# Plot
plt.figure(figsize=(12,6))

for country in top10_countries:
    data = df_top10[df_top10['Country'] == country]
    plt.plot(data['Year'], data['Population'], label=country)

plt.legend()
plt.title("Population Trend of Top 10 Countries")
plt.xlabel("Year")
plt.ylabel("Population")

pdf.savefig()
plt.close()
# Average Population Table
# avg_pop_country = df.groupby('Country')['Population'].mean().reset_index().head(10)
# save_table(avg_pop_country, "Average Population by Country (Top 10)")

# ------------------------------------------------------------
# MAX / MIN POPULATION (WITH COUNTRY + YEAR)
# ------------------------------------------------------------

# Get row with maximum population
max_row = df.loc[df['Population'].idxmax()]

# Get row with minimum population
min_row = df.loc[df['Population'].idxmin()]

# Create table
min_max_df = pd.DataFrame({
    "Metric": ["Max Population", "Min Population"],
    "Country": [max_row['Country'], min_row['Country']],
    "Year": [int(max_row['Year']), int(min_row['Year'])],
    "Population": [max_row['Population'], min_row['Population']]
})

# Save table
save_table(min_max_df, "Population Extremes with Country and Year")
# # Max / Min Table
# min_max_df = pd.DataFrame({
#     "Metric": ["Max Population", "Min Population"],
#     "Value": [df['Population'].max(), df['Population'].min()]
# })
# save_table(min_max_df, "Population Extremes")


# Top 10 Countries
latest_year = df['Year'].max()
top10 = df[df['Year'] == latest_year].sort_values(by='Population', ascending=False).head(10)

plt.figure()
plt.bar(top10['Country'], top10['Population'])
plt.xticks(rotation=45)
plt.title("Top 10 Most Populated Countries")
pdf.savefig()
plt.close()

save_table(top10[['Country', 'Population']], "Top 10 Most Populated Countries")


# Bottom 10 Countries
bottom10 = df[df['Year'] == latest_year].sort_values(by='Population').head(10)

plt.figure()
plt.bar(bottom10['Country'], bottom10['Population'])
plt.xticks(rotation=45)
plt.title("Bottom 10 Least Populated Countries")
pdf.savefig()
plt.close()

save_table(bottom10[['Country', 'Population']], "Bottom 10 Least Populated Countries")


# ============================================================
# PART 2: GROWTH ANALYSIS
# ============================================================

# # Growth Table (Sample)
# growth_sample = df[['Country', 'Year', 'Growth Rate (%)']].dropna().head(10)
# save_table(growth_sample, "Sample Growth Rate Data")
# ------------------------------------------------------------
# AVG GROWTH BY COUNTRY (DEFINE FIRST)
# ------------------------------------------------------------

avg_growth_country = df.groupby('Country')['Growth Rate (%)'] \
    .mean() \
    .sort_values(ascending=False) \
    .reset_index() \
    .head(10)

# OPTIONAL: sort for better visualization
avg_growth_country = avg_growth_country.sort_values(by='Growth Rate (%)')

# ------------------------------------------------------------
# GRAPH
# ------------------------------------------------------------

plt.figure(figsize=(10,6))

sns.barplot(
    data=avg_growth_country,
    x='Growth Rate (%)',
    y='Country'
)

plt.title("Top 10 Countries by Average Population Growth Rate")
plt.xlabel("Average Growth Rate (%)")
plt.ylabel("Country")

pdf.savefig()
plt.close()

# Avg Growth by Country
avg_growth_country = df.groupby('Country')['Growth Rate (%)'].mean().sort_values(ascending=False).reset_index().head(10)
avg_growth_country['Growth Rate (%)'] = avg_growth_country['Growth Rate (%)'].round(2)
save_table(avg_growth_country, "Top 10 Countries by Growth Rate")


# Avg Growth by Continent
avg_growth_continent = df.groupby('Continent')['Growth Rate (%)'].mean().reset_index()

plt.figure()
plt.bar(avg_growth_continent['Continent'], avg_growth_continent['Growth Rate (%)'])
plt.title("Average Growth Rate by Continent")
pdf.savefig()
plt.close()

# save_table(avg_growth_continent, "Average Growth Rate by Continent")

# ------------------------------------------------------------
# NEGATIVE GROWTH COUNTRIES (GRAPH)
# ------------------------------------------------------------

# Get countries with negative growth
neg_df = df[df['Growth Rate (%)'] < 0]

# Calculate average negative growth per country
neg_growth = neg_df.groupby('Country')['Growth Rate (%)'].mean().reset_index()

# Sort (most negative first)
neg_growth = neg_growth.sort_values(by='Growth Rate (%)')

# Take top 15 worst affected countries
neg_growth = neg_growth.head(15)

# Plot
plt.figure(figsize=(10,6))

sns.barplot(
    data=neg_growth,
    x='Growth Rate (%)',
    y='Country'
)

plt.title("Top 15 Countries with Negative Population Growth")
plt.xlabel("Growth Rate (%)")
plt.ylabel("Country")

pdf.savefig()
plt.close()
# # Negative Growth Countries
# negative_growth = pd.DataFrame(df[df['Growth Rate (%)'] < 0]['Country'].unique(), columns=['Country'])
# save_table(negative_growth.head(15), "Countries with Negative Growth")

# ------------------------------------------------------------
# HIGHEST & LOWEST GROWTH (WITH YEAR)
# ------------------------------------------------------------

# Get row with highest growth
max_row = df.loc[df['Growth Rate (%)'].idxmax()]

# Get row with lowest growth
min_row = df.loc[df['Growth Rate (%)'].idxmin()]

# Create table
extreme_growth = pd.DataFrame({
    "Type": ["Highest Growth", "Lowest Growth"],
    "Country": [max_row['Country'], min_row['Country']],
    "Year": [int(max_row['Year']), int(min_row['Year'])],
    "Growth Rate (%)": [max_row['Growth Rate (%)'], min_row['Growth Rate (%)']]
})

# Save table
save_table(extreme_growth, "Growth Extremes with Year")
# # Highest / Lowest Growth
# extreme_growth = pd.DataFrame({
#     "Type": ["Highest Growth", "Lowest Growth"],
#     "Country": [
#         df.groupby('Country')['Growth Rate (%)'].mean().idxmax(),
#         df.groupby('Country')['Growth Rate (%)'].mean().idxmin()
#     ]
# })
# save_table(extreme_growth, "Growth Extremes")


# Growth Distribution Plot
plt.figure()
sns.histplot(df['Growth Rate (%)'].dropna(), bins=50)
plt.title("Growth Rate Distribution")
pdf.savefig()
plt.close()


# ============================================================
# PART 3: COMPARATIVE ANALYSIS
# ============================================================

# Compare 5 Countries
countries = ['India', 'China', 'United States', 'Germany', 'Brazil']
subset = df[df['Country'].isin(countries)]

plt.figure()
for country in countries:
    data = subset[subset['Country'] == country]
    plt.plot(data['Year'], data['Population'], label=country)

plt.legend()
plt.title("Population Trend Comparison")
plt.xlabel("Year")
plt.ylabel("Population")
pdf.savefig()
plt.close()


# Continent Growth
continent_growth = df.groupby(['Continent', 'Year'])['Population'].sum().reset_index()

plt.figure()
for continent in continent_growth['Continent'].unique():
    data = continent_growth[continent_growth['Continent'] == continent]
    plt.plot(data['Year'], data['Population'], label=continent)

plt.legend()
plt.title("Population Growth by Continent")
plt.xlabel("Year")
plt.ylabel("Population")
pdf.savefig()
plt.close()





# ============================================================
# PART 4: ADVANCED ANALYSIS (ADDED TO SAME PDF)
# ============================================================

# ------------------------------------------------------------
# 1. OUTLIERS IN GROWTH RATE (FINAL FIXED)
# ------------------------------------------------------------

# Step 1: Calculate IQR
Q1 = df['Growth Rate (%)'].quantile(0.25)
Q3 = df['Growth Rate (%)'].quantile(0.75)
IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

# Step 2: Detect outliers
outliers = df[
    (df['Growth Rate (%)'] < lower) | 
    (df['Growth Rate (%)'] > upper)
]

# Step 3: Work on copy (avoid warning)
outliers = outliers.copy()

# Step 4: Get extreme outliers per country
outliers['Abs Growth'] = outliers['Growth Rate (%)'].abs()

top_outliers = outliers.sort_values(by='Abs Growth', ascending=False)

# Get top 20 unique countries
top_outliers = top_outliers.drop_duplicates(subset='Country').head(20)

# Step 5: Save table
save_table(
    top_outliers[['Country', 'Year', 'Growth Rate (%)']],
    "Top 20 Countries with Extreme Population Growth Outliers"
)

# Step 6: Plot
plt.figure(figsize=(10,6))

sns.barplot(
    data=top_outliers,
    x='Growth Rate (%)',
    y='Country'
)

plt.title("Top 20 Outlier Countries by Growth Rate")

pdf.savefig()
plt.close()


# ------------------------------------------------------------
# 2. LONG-TERM GROWTH RANKING
# ------------------------------------------------------------
# ------------------------------------------------------------
# LONG-TERM GROWTH WITH START/END YEAR + %
# ------------------------------------------------------------

# Ensure sorted (VERY IMPORTANT)
df_sorted = df.sort_values(by=['Country', 'Year'])

growth_rank = df_sorted.groupby('Country').agg(
    start_year=('Year', 'first'),
    end_year=('Year', 'last'),
    start_pop=('Population', 'first'),
    end_pop=('Population', 'last')
)

# Absolute Growth
growth_rank['Total Growth'] = growth_rank['end_pop'] - growth_rank['start_pop']

# Percentage Growth
growth_rank['Growth (%)'] = (
    (growth_rank['end_pop'] - growth_rank['start_pop']) 
    / growth_rank['start_pop']
) * 100

# Sort by total growth
growth_rank = growth_rank.sort_values(by='Total Growth', ascending=False).reset_index()
growth_rank['Growth (%)'] = growth_rank['Growth (%)'].round(2)
# Save table
save_table(
    growth_rank.head(10),
    "Top 10 Countries by Long-Term Population Growth"
)
# growth_rank = df.groupby('Country').agg(
#     start_pop=('Population', 'first'),
#     end_pop=('Population', 'last')
# )

# growth_rank['Total Growth'] = growth_rank['end_pop'] - growth_rank['start_pop']
# growth_rank = growth_rank.sort_values(by='Total Growth', ascending=False).reset_index()

# save_table(growth_rank.head(10), "Top 10 Countries by Long-Term Growth")


# ------------------------------------------------------------
# 3. ABSOLUTE vs PERCENTAGE GROWTH
# ------------------------------------------------------------
df['Absolute Growth'] = df.groupby('Country')['Population'].diff()

comparison = df[['Country', 'Year', 'Absolute Growth', 'Growth Rate (%)']].dropna()

plt.figure()
sns.scatterplot(data=comparison, x='Absolute Growth', y='Growth Rate (%)')
plt.title("Absolute vs Percentage Growth")
pdf.savefig()
plt.close()


# ------------------------------------------------------------
# 4. POPULATION DOUBLING TIME
# ------------------------------------------------------------
# ------------------------------------------------------------
# DOUBLING TIME FOR ALL COUNTRIES
# ------------------------------------------------------------

# Remove negative & zero growth
df_valid = df[df['Growth Rate (%)'] > 0]

# Recalculate doubling time
df_valid['Doubling Time'] = 70 / df_valid['Growth Rate (%)']

# Aggregate
doubling_all = df_valid.groupby('Country')['Doubling Time'].mean().reset_index()

# Sort correctly
doubling_all = doubling_all.sort_values(by='Doubling Time')

# Plot
plt.figure(figsize=(10,6))

sns.barplot(
    data=doubling_all.head(15),
    x='Doubling Time',
    y='Country'
)

plt.title("Top 15 Countries by Fastest Population Doubling")

pdf.savefig()
plt.close()

# ------------------------------------------------------------
# DOUBLING TIME ANALYSIS (TOP 10 COUNTRIES)
# ------------------------------------------------------------

# Step 1: Get top 10 countries by latest population
latest_year = df['Year'].max()

top10_countries = df[df['Year'] == latest_year] \
    .sort_values(by='Population', ascending=False) \
    .head(10)['Country']

df_top10 = df[df['Country'].isin(top10_countries)]

# Step 2: Calculate average growth rate per country
avg_growth = df_top10.groupby('Country')['Growth Rate (%)'].mean().reset_index()

# Step 3: Calculate Doubling Time (Rule of 70)
avg_growth['Doubling Time (Years)'] = 70 / avg_growth['Growth Rate (%)']

# Handle invalid values
avg_growth['Doubling Time (Years)'] = avg_growth['Doubling Time (Years)'] \
    .replace([float('inf'), -float('inf')], None)

# Sort by doubling time
avg_growth = avg_growth.sort_values(by='Doubling Time (Years)')

# ------------------------------------------------------------
# SAVE TABLE
# ------------------------------------------------------------
avg_growth['Growth Rate (%)'] = avg_growth['Growth Rate (%)'].round(2)
avg_growth['Doubling Time (Years)'] = avg_growth['Doubling Time (Years)'].round(2)
save_table(avg_growth, "Population Doubling Time (Top 10 Countries)")


# ------------------------------------------------------------
# VISUALIZATION (BAR CHART)
# ------------------------------------------------------------
plt.figure(figsize=(10, 6))

sns.barplot(
    data=avg_growth,
    x='Doubling Time (Years)',
    y='Country'
)

plt.title("Population Doubling Time (Top 10 Countries)")
plt.xlabel("Years to Double Population")
plt.ylabel("Country")

pdf.savefig()
plt.close()


# ------------------------------------------------------------
# 5. POPULATION vs GROWTH RELATIONSHIP
# ------------------------------------------------------------
plt.figure()
sns.scatterplot(data=df, x='Population', y='Growth Rate (%)')
plt.title("Population vs Growth Rate")
pdf.savefig()
plt.close()


# ------------------------------------------------------------
# 6. HEATMAP (TOP 20 COUNTRIES)
# ------------------------------------------------------------
# ------------------------------------------------------------
# IMPROVED HEATMAP (HIGH QUALITY)
# ------------------------------------------------------------

# Select top 15 countries by population (cleaner visualization)
top_countries = df.groupby('Country')['Population'].mean().sort_values(ascending=False).head(15).index

pivot = df[df['Country'].isin(top_countries)].pivot_table(
    values='Growth Rate (%)',
    index='Country',
    columns='Year'
)

plt.figure(figsize=(16, 8))

sns.heatmap(
    pivot,
    cmap='RdYlGn',          # Better color contrast (red → green)
    linewidths=0.5,         # Grid lines
    linecolor='gray',
    cbar_kws={'label': 'Growth Rate (%)'},
    annot=False             # Turn ON only if small dataset
)

plt.title("Population Growth Rate Heatmap (Top 15 Countries)", fontsize=16)
plt.xlabel("Year")
plt.ylabel("Country")

plt.xticks(rotation=45)
plt.yticks(rotation=0)

pdf.savefig()
plt.close()

# pivot = df.pivot_table(
#     values='Growth Rate (%)',
#     index='Country',
#     columns='Year'
# )

# pivot_sample = pivot.head(20)

# plt.figure(figsize=(12, 6))
# sns.heatmap(pivot_sample, cmap='coolwarm')
# plt.title("Growth Rate Heatmap (Top 20 Countries)")
# pdf.savefig()
# plt.close()


# ============================================================
# SAVE PDF
# ============================================================

pdf.close()

print("✅ FULL REPORT GENERATED: EDA_Analysis_Report.pdf")




# ============================================================
# PART 5: DATA VISUALIZATION (FINAL - BILLIONS FORMAT)
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.ticker as ticker

# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(r"E:\Masters\UE\Data Analytics\Final submission\API_SP.POP.TOTL_DS2_en_csv_v2_406129\Cleaned_Population_Data.csv")

pdf = PdfPages("Part5_DataVisualization.pdf")


# ============================================================
# 1. LINE CHART → GLOBAL POPULATION (IN BILLIONS)
# ============================================================

total_pop_year = df.groupby('Year')['Population'].sum() / 1e9

plt.figure()
plt.plot(total_pop_year.index, total_pop_year.values, label='Population (Billions)')
plt.legend()

plt.title("Global Population Growth Over Time")
plt.xlabel("Year")
plt.ylabel("Population (Billions)")

plt.figtext(0.1, -0.1,
"Interpretation: Global population has steadily increased over time, showing continuous growth worldwide.",
wrap=True)

pdf.savefig()
plt.close()


# ============================================================
# 2. BAR CHART → TOP COUNTRIES (IN BILLIONS)
# ============================================================

latest_year = df['Year'].max()

top10 = df[df['Year'] == latest_year] \
    .sort_values(by='Population', ascending=False) \
    .head(10)

top10['Population_B'] = top10['Population'] / 1e9

plt.figure(figsize=(10,6))

sns.barplot(
    data=top10,
    x='Population_B',
    y='Country',
    hue='Country',
    dodge=False,
    legend=False
)

plt.title("Top 10 Most Populated Countries")
plt.xlabel("Population (Billions)")
plt.ylabel("Country")

plt.figtext(0.1, -0.1,
"Interpretation: A few countries dominate global population, with significant differences among them.",
wrap=True)

pdf.savefig()
plt.close()


# ------------------------------------------------------------
# 3. PIE CHART → DISTRIBUTION (FIXED)
# ------------------------------------------------------------

# Use only required columns
top5 = top10[['Country', 'Population']].head(5).copy()

# Calculate rest of world
total_population = df[df['Year'] == latest_year]['Population'].sum()
rest = total_population - top5['Population'].sum()

# Add new row correctly
rest_row = pd.DataFrame({
    'Country': ['Rest of World'],
    'Population': [rest]
})

pie_data = pd.concat([top5, rest_row], ignore_index=True)

# Convert to billions
pie_data['Population_B'] = pie_data['Population'] / 1e9

# Plot
plt.figure()

plt.pie(
    pie_data['Population_B'],
    labels=pie_data['Country'],
    autopct='%1.1f%%'
)

plt.title("Global Population Distribution (Top 5 + Rest of World)")

plt.figtext(0.1, -0.1,
"Interpretation: The chart shows that a few countries contribute a large share of global population, while the rest of the world collectively forms a significant portion.",
wrap=True)

pdf.savefig()
plt.close()


# ============================================================
# 4. SCATTER → POPULATION vs GROWTH
# ============================================================

df['Population_B'] = df['Population'] / 1e9

plt.figure()

sns.scatterplot(
    data=df,
    x='Population_B',
    y='Growth Rate (%)',
    hue='Continent'
)

plt.legend(title="Continent")

plt.title("Population vs Growth Rate by Continent")
plt.xlabel("Population (Billions)")
plt.ylabel("Growth Rate (%)")

plt.figtext(0.1, -0.1,
"Interpretation: Larger populations tend to have moderate growth rates, while smaller countries show higher variation.",
wrap=True)

pdf.savefig()
plt.close()


# ============================================================
# 5. HEATMAP → GROWTH PATTERN
# ============================================================

top_countries = df.groupby('Country')['Population'] \
    .mean() \
    .sort_values(ascending=False) \
    .head(15) \
    .index

pivot = df[df['Country'].isin(top_countries)].pivot_table(
    values='Growth Rate (%)',
    index='Country',
    columns='Year'
)

plt.figure(figsize=(14,7))

sns.heatmap(
    pivot,
    cmap='RdYlGn',
    linewidths=0.5,
    cbar_kws={'label': 'Growth Rate (%)'}
)

plt.title("Growth Rate Heatmap (Top 15 Countries)")
plt.xlabel("Year")
plt.ylabel("Country")

plt.figtext(0.1, -0.15,
"Interpretation: The heatmap highlights variations in growth rates across countries over time.",
wrap=True)

pdf.savefig()
plt.close()


# ============================================================
# 6. FORECAST → FUTURE POPULATION (IN BILLIONS)
# ============================================================

country_data = df[df['Country'] == 'India']

X = country_data['Year'].values.reshape(-1,1)
y = country_data['Population'].values / 1e9  # convert to billions

model = LinearRegression()
model.fit(X, y)

future_years = np.arange(2025, 2035).reshape(-1,1)
future_pred = model.predict(future_years)

plt.figure()

plt.plot(country_data['Year'], y, label='Actual Population (Billions)')
plt.plot(future_years, future_pred, linestyle='--', label='Predicted Population (Billions)')

plt.legend()

plt.title("Population Forecast for India")
plt.xlabel("Year")
plt.ylabel("Population (Billions)")

plt.figtext(0.1, -0.1,
"Interpretation: The forecast suggests continued population growth in the future based on historical trends.",
wrap=True)

pdf.savefig()
plt.close()


# ============================================================
# SAVE PDF
# ============================================================

pdf.close()

print("✅ FINAL PART 5 PDF GENERATED (NO 1e9, CLEAN UNITS)")


# ============================================================
# PART 6: PREDICTION & FORECASTING
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from sklearn.linear_model import LinearRegression
import numpy as np

# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(r"E:\Masters\UE\Data Analytics\Final submission\API_SP.POP.TOTL_DS2_en_csv_v2_406129\Cleaned_Population_Data.csv")

pdf = PdfPages("Part6_Forecasting.pdf")


# ============================================================
# SELECT COUNTRY (YOU CAN CHANGE)
# ============================================================

country_name = "India"
country_data = df[df['Country'] == country_name].sort_values('Year')

# Convert to billions for better readability
country_data['Population_B'] = country_data['Population'] / 1e9


# ============================================================
# PREPARE DATA
# ============================================================

X = country_data['Year'].values.reshape(-1,1)
y = country_data['Population_B'].values


# ============================================================
# TRAIN MODEL (LINEAR REGRESSION)
# ============================================================

model = LinearRegression()
model.fit(X, y)


# ============================================================
# FORECAST NEXT 10 YEARS
# ============================================================

future_years = np.arange(country_data['Year'].max()+1, country_data['Year'].max()+11).reshape(-1,1)
future_pred = model.predict(future_years)


# ============================================================
# CREATE FORECAST TABLE
# ============================================================

forecast_df = pd.DataFrame({
    'Year': future_years.flatten(),
    'Predicted Population (Billions)': future_pred.round(2)
})

print("\nForecasted Population:")
print(forecast_df)


# ============================================================
# SAVE TABLE INTO PDF
# ============================================================

def save_table(df_table, title):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.axis('tight')
    ax.axis('off')

    table = ax.table(
        cellText=df_table.values,
        colLabels=df_table.columns,
        loc='center'
    )

    table.auto_set_font_size(False)
    table.set_fontsize(10)

    plt.title(title)
    pdf.savefig()
    plt.close()

save_table(forecast_df, f"Population Forecast for {country_name} (Next 10 Years)")


# ============================================================
# VISUALIZATION (ACTUAL vs FORECAST)
# ============================================================

plt.figure()

# Actual
plt.plot(country_data['Year'], y, label='Actual Population (Billions)')

# Forecast
plt.plot(future_years, future_pred, linestyle='--', label='Predicted Population (Billions)')

plt.legend()

plt.title(f"Population Forecast for {country_name}")
plt.xlabel("Year")
plt.ylabel("Population (Billions)")

plt.figtext(0.1, -0.1,
"Interpretation: The forecast indicates a steady increase in population based on past trends, suggesting continued growth in the coming years.",
wrap=True)

pdf.savefig()
plt.close()


# ============================================================
# LIMITATIONS PAGE
# ============================================================

limitations_text = [
    "Limitations of Prediction Model:",
    "",
    "1. Linear regression assumes constant growth, which may not reflect real-world changes.",
    "2. It does not consider external factors like migration, government policies, or economic conditions.",
    "3. Predictions become less accurate for long-term forecasting.",
    "4. Unexpected events (pandemics, conflicts) can significantly impact population trends."
]

fig, ax = plt.subplots(figsize=(10,6))
ax.axis('off')

for i, line in enumerate(limitations_text):
    ax.text(0.01, 0.9 - i*0.1, line, fontsize=11)

pdf.savefig()
plt.close()


# ============================================================
# SAVE PDF
# ============================================================

pdf.close()

print("✅ PART 6 COMPLETED: Part6_Forecasting.pdf GENERATED")