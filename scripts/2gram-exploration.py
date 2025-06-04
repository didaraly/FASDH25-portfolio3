
# What are the most frequent conflict-related terms, and how do their frequencies change over time.

#import necessary libraries
import pandas as pd  
import plotly.express as px  

# Load and read 2-gram data from CSV file into DataFrame for analysis. 
df_2gram = pd.read_csv("../data/dataframes/n-grams/2-gram/2-gram.csv")

# Removes rows with zero count from 2-gram DataFrames to keep only relevant data.
df_2gram = df_2gram[df_2gram['count'] > 0]

# Makes all 2-gram words lowercase for consistency.
df_2gram['2-gram'] = df_2gram['2-gram'].str.lower()
  
# Defines a list of key 2-gram conflict-related terms for focused analysis.  
conflict_terms = ['israel attack', 'humanitarian aid', 'children killed', 'attacked gaza']  

# Filters the 2-gram DataFrame to keep only rows with specified conflict-related terms. 
df_conflict_2gram = df_2gram[df_2gram['2-gram'].isin(conflict_terms)]


# Groups 2-gram data by year, month, and term, summing their counts.  
df_grouped = df_conflict_2gram.groupby(['year', 'month', '2-gram'])['count'].sum().reset_index()

# Creates a datetime column from year and month to analyse easily.
df_grouped['date'] = pd.to_datetime(df_grouped[['year', 'month']].assign(day= 1))  

# Plots a line chart of conflict-related 2-gram frequencies over time. 
fig = px.line(df_grouped, x='date', y='count', color='2-gram',  
              title='Conflict-Related Terms Frequency Over Time',  
              labels={'count': 'Frequency', 'date': 'Month'})  
fig.show()  # Shows the line chart.

fig.write_html("../outputs/ngrams/exploration/conflict_terms_2grams_over_time.html") # Saves the 2-gram conflict terms chart as an HTML file.

# Saves the grouped 2-gram data to a CSV file without the index.
df_grouped.to_csv("../outputs/ngrams/exploration/conflict_terms_2grams_frequency_exploration_over_time.csv", index=False)

# Selects data from October 2023 onward to analyze the war period. 
df_war_period = df_grouped[df_grouped['date'] >= '2023-10-01']

# Creates a line chart for conflict 2-gram frequencies during the war period starting October 2023 to view.
fig_war = px.line(df_war_period, x='date', y='count', color='2-gram',  
                  title='Conflict-Related Terms Frequency Since October 2023 (War Period)',  
                  labels={'count': 'Frequency', 'date': 'Month'})  

fig_war.show()  # Shows the line chart of 2gram conflict term during war period.

# Saves the war period 2-gram conflict terms chart as an HTML file.
fig_war.write_html("../outputs/ngrams/exploration/conflict_terms_2grams_war_period_only.html")

# Saves the war period 2-gram conflict data to a CSV file without the index.
df_war_period.to_csv("../outputs/ngrams/exploration/conflict_terms_frequency_2grams_war_period_only.csv", index=False)





