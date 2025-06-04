
# What are the most frequent conflict-related terms, and how do their frequencies change over time?

# import necessary libraries
import pandas as pd  
import plotly.express as px  


# Load and read 1-gram data for analysis from CSV into a DataFrame
df_1gram = pd.read_csv("../data/dataframes/n-grams/1-gram/1-gram.csv")

# Removes rows with zero count from 1-gram DataFrames to keep only relevant data.
df_1gram = df_1gram[df_1gram['count'] > 0]

# Makes all 1-gram words lowercase for consistency.
df_1gram['1-gram'] = df_1gram['1-gram'].str.lower()

# List of common English stop words (from NLTK) to remove from 1-gram list
stop_words = [
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your",
    "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her",
    "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs",
    "themselves", "what", "which", "who", "whom", "this", "that", "these", "those",
    "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
    "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if",
    "or", "because", "as", "until", "while", "of", "at", "by", "for", "with",
    "about", "against", "between", "into", "through", "during", "before", "after",
    "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over",
    "under", "again", "further", "then", "once", "here", "there", "when", "where",
    "why", "how", "all", "any", "both", "each", "few", "more", "most", "other",
    "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too",
    "very", "of", "the", "can", "will", "just", "don", "should", "now","and","in", "s","said"
]

# Remove stop words from the 1-gram DataFrame for cleaner analysis.
df_no_stop = df_1gram[~df_1gram["1-gram"].isin(stop_words)]

# Group by 1-gram and sum their counts from the cleaned (no stopwords) DataFrame.
top_1grams = df_no_stop.groupby('1-gram')['count'].sum().reset_index()

# Sort in descending order and get the top 5
top_5_1grams = top_1grams.sort_values(by='count', ascending=False).head(5)

print(top_5_1grams)
  
# Define list conflict-related terms  for focused analysis.  
conflict_terms = ['attack', 'ceasefire', 'humanitarian', 'casualties', 'aid', 'blockade', 'genocide', 'israel', 'children', 'killed']  

# Filter 1-grams to only include conflict-related terms 
df_conflict_1gram = df_1gram[df_1gram['1-gram'].isin(conflict_terms)]


# Groups conflict-related 1-grams by year, month, and term, summing their counts.  
df_grouped = df_conflict_1gram.groupby(['year', 'month', '1-gram'])['count'].sum().reset_index()

# Creates a datetime column from year and month for time-based analysis.
df_grouped['date'] = pd.to_datetime(df_grouped[['year', 'month']].assign(day= 1))  

# Plots a line chart to visualize how conflict-related term frequencies change over time.
fig = px.line(df_grouped, x='date', y='count', color='1-gram',  
              title='Conflict-Related Term Frequency Over Time',  
              labels={'count': 'Frequency', 'date': 'Month'})  

fig.show()  # Shows the line chart.

# Saves the chart as an HTML file to view.
fig.write_html("../outputs/ngrams/exploration/conflict_terms_1gram_over_time.html")

# Saves the grouped data to a CSV file without the index.
df_grouped.to_csv("../outputs/ngrams/exploration/conflict_terms_frequency_1gram_exploration_over_time.csv", index=False)

# Selects data from October 2023 onwards to focus on the war period.
df_war_period = df_grouped[df_grouped['date'] >= '2023-10-01']

# Creates a line chart showing conflict term frequencies during the war period starting October 2023.
fig_war = px.bar(df_war_period, x='date', y='count', color='1-gram',  
                  title='Conflict-Related Terms Frequency Since October 2023 (War Period)',  
                  labels={'count': 'Frequency', 'date': 'Month'},
                 barmode='group')

fig_war.show()  # Shows the line chart.
fig_war.write_html("../outputs/ngrams/exploration/conflict_terms_1grams_war_period_only.html") # Saves the chart as an HTML file to view.

# Saves the war period conflict term frequencies to a CSV file without the index.
df_war_period.to_csv("../outputs/ngrams/exploration/conflict_terms_frequency_1gram_exploration_war_period_only.csv", index=False)




