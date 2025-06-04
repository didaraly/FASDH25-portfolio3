#How did the frequency of “Casualties” and “Humanitarian aid” change during the 2023-24 conflict?

# Imports pandas for data handling and plotly.express for data visualization
import pandas as pd
import plotly.express as px

# Loads 1-gram and 2-gram datasets from CSV files into DataFrames for analysis. 
df_1gram = pd.read_csv("../data/dataframes/n-grams/1-gram/1-gram.csv")  
df_2gram = pd.read_csv("../data/dataframes/n-grams/2-gram/2-gram.csv")

# Removes rows with zero count from both 1-gram and 2-gram DataFrames to keep only relevant data.
df_1gram = df_1gram[df_1gram['count'] > 0]
df_2gram = df_2gram[df_2gram['count'] > 0]

# Makes all 1-gram and 2-gram words lowercase for consistency.
df_1gram['1-gram'] = df_1gram['1-gram'].str.lower()
df_2gram['2-gram'] = df_2gram['2-gram'].str.lower()

# Filters the 1-gram data to keep only rows where the word is 'casualties'.
casualties = df_1gram[df_1gram['1-gram'] == 'casualties']

# Filters the 2-gram data to keep only rows where the phrase is 'humanitarian aid'.
humanitarian_aid = df_2gram[df_2gram['2-gram'] == 'humanitarian aid']

# Adds a new column 'term' to label the filtered rows for easy identification.
casualties['term'] = 'casualties'
humanitarian_aid['term'] = 'humanitarian aid'

# Renames 'count' column (no actual change) to keep things clear or consistent.
casualties = casualties.rename(columns={'count': 'count'})
humanitarian_aid = humanitarian_aid.rename(columns={'count': 'count'})

# Combines the casualties and humanitarian aid data into one DataFrame.
combined = pd.concat([casualties, humanitarian_aid])

# Creates a date column from year and month for easier time analysis.
combined['date'] = pd.to_datetime(combined[['year', 'month']].assign(day=1))

# Filters data to include war-time dates only from October 2023 onwards.
combined = combined[combined['date'] >= '2023-10-01']

# Groups data by date and term, summing counts to get total frequency per term each month.
combined = combined.groupby(['date', 'term'])['count'].sum().reset_index()

# Creates a line chart comparing monthly mentions of "Casualties" and "Humanitarian Aid" during the war.
fig = px.line(
    combined,
    x='date',
    y='count',
    color='term',
    title='Mentions of "Casualties" vs "Humanitarian Aid" during war period',
    labels={'count': 'Frequency', 'date': 'Month', 'term': 'Term'}
)

# Saves the comparison chart as an HTML file for easy visualization.
fig.write_html("../outputs/ngrams/visualization/Visualization_Humanitarian_Aid_vs_Casualties_output.html")

# Show the comparison chart.
fig.show()

combined.to_csv("../outputs/ngrams/exploration/Humanitarian_Aid_vs_Casualties_war_period_only.csv", index=False)

