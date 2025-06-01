
# Question: What are the most frequent conflict-related
#  terms, and how do their frequencies change over time?

#import necessary libraries
import pandas as pd  
import plotly.express as px  

# read 1-gram, 2-gram, and 3-gram data  
df_1gram = pd.read_csv("../data/dataframes/n-grams/1-gram/1-gram.csv")  
df_2gram = pd.read_csv("../data/dataframes/n-grams/2-gram/2-gram.csv")  
df_3gram = pd.read_csv("../data/dataframes/n-grams/3-gram/3-gram.csv")  



# Define conflict-related terms  
conflict_terms = ['attack', 'ceasefire', 'humanitarian', 'casualties', 'aid', 'blockade', 'genocide']  

# Filter 1-grams to only include conflict-related terms 
df_conflict_1gram = df_1gram[df_1gram['1-gram'].isin(conflict_terms)]


# Group by year-month and sum counts  
df_grouped = df_conflict_1gram.groupby(['year', 'month', '1-gram'])['count'].sum().reset_index()  
df_grouped['date'] = pd.to_datetime(df_grouped[['year', 'month']].assign(day= 1))  

# Line chart for term frequency  
fig = px.line(df_grouped, x='date', y='count', color='1-gram',  
              title='Conflict-Related Term Frequency Over Time',  
              labels={'count': 'Frequency', 'date': 'Month'})  
fig.show()  
fig.write_html("conflict_terms_output.html")
# Compare with 2-grams (e.g., "humanitarian crisis")  
df_crisis = df_2gram[df_2gram['2-gram'] == 'humanitarian crisis']  
fig = px.bar(df_crisis, x='month', y='count', color='year',  
             title='Frequency of "Humanitarian Crisis" by Month',)  
fig.show()  
fig.write_html("humanitarian_crisis_output.html")
# Export exploration results to outputs as CSV File
df_grouped.to_csv("../outputs/conflict_terms_frequency_exploration.csv", index=False)
# Filter terms  
ceasefire = df_1gram[df_1gram['1-gram'] == 'ceasefire']  
humanitarian_aid = df_2gram[df_2gram['2-gram'] == 'humanitarian aid']  

# Combine data  
combined = pd.concat([  
    ceasefire.rename(columns={'1-gram': 'term', 'count': 'ceasefire_count'}),  
    humanitarian_aid.rename(columns={'2-gram': 'term', 'count': 'aid_count'})  
])  

# Plot dual-axis chart  
fig = px.scatter(combined, x='month', y=['ceasefire_count', 'aid_count'], color='term',  
              facet_col='year',  
              title='Frequency of "Ceasefire" vs. "Humanitarian Aid" (2023)')  
fig.update_layout(yaxis_title='Frequency', legend_title='Term')  
  
fig.write_html("Humanitarian_crises_vs_ceasefire_output.html")




