# Import required libraries
import pandas as pd # for data manipulation
import plotly.express as px # for interactive visualizations

# Load data (topic modeling from CSV)
df = pd.read_csv("../data/dataframes/topic-model/topic-model.csv")

# Initial Cleaning
# remove noise labeled as topic -1
df = df[df['Topic'] != -1]
# check the structure and content of the cleaned dataset
print(df)
# Define stopwords to eliminate generic and non-informative words:
stop_words = [   # common English stopwords from NLTK to filter out irrelevant topics
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
    "very", "s", "to", "can", "will", "just", "don", "should", "now"]

# Filter out rows where any of the top 4 keywords are stopwords
df = df[~df['topic_1'].str.lower().isin(stop_words)]
df = df[~df['topic_2'].str.lower().isin(stop_words)]
df = df[~df['topic_3'].str.lower().isin(stop_words)]
df = df[~df['topic_4'].str.lower().isin(stop_words)]
# Create a combined topic label
df['Topic_Label'] = df['topic_1'] + ', ' + df['topic_2'] + ',' + df['topic_3'] + ',' + df['topic_4']
# Print and check
print(df)


#Which topics dominated coverage in 2023, and how do they compare to 2024?  (Top topics in 2023 vs. 2024)
# ensure noise topics are removed again
df = df[df['Topic'] != -1]  
# regenerate topic label
df['Topic_Label'] = df['topic_1'] + ', ' + df['topic_2']  + ',' + df['topic_3'] + ',' + df['topic_4']
# Check
print(df['Topic_Label'])
# Count topic occurrences for each year
# Count topic occurrences for 2023
df_2023 = df[df['year'] == 2023]['Topic_Label'].value_counts().reset_index(name='count')
df_2023['year'] = 2023
# Print and check
print(df_2023)
# Count topic occurrences for 2024
df_2024 = df[df['year'] == 2024]['Topic_Label'].value_counts().reset_index(name='count')
df_2024['year'] = 2024
# Print and check
print(df_2024)
# Combine and rename columns
df_combined = pd.concat([df_2023, df_2024])
df_combined.columns = ['Topic_Label', 'Count', 'Year']
# Print and check
print(df_combined)
# Plot: Year on x-axis, Count on y-axis, Topic_Label as color
fig = px.bar(df_combined, 
             x='Year', 
             y='Count', 
             color='Topic_Label',
             title='Dominant Topics in 2023 vs. 2024',
             labels={'Year': 'Year', 'Count': 'Frequency', 'Topic_Label': 'Topic'},
             barmode='group')
# Ensure x-axis is treated as categorical (not continuous) for proper bar grouping
fig.update_layout(xaxis=dict(type='category'))
# save chart as html
fig.write_html("../outputs/topic-modelling/visualization/topic_dominance_2023vs2024.html")  
# save as csv
df_combined.to_csv("../outputs/topic-modelling/exploration/topic_dominance_2023vs2024.csv")


#Top 20 Topics in Entire Dataset
# Get top 20 topic labels
top_20 = df['Topic_Label'].value_counts().head(20).reset_index()
# Print for verification
print(top_20)
# Rename columns for clarity
top_20.columns = ['Topic_Label', 'Count']
# Confirm column renaming
print(top_20.columns)
# Create bar chart for top 20 topics
fig_20 = px.bar(top_20, 
                x='Topic_Label', y='Count',
                title='Top 20 Dominant Topics in Entire Dataset',
                labels={'Topic_Label': 'Topic'},
                hover_data={'Count': True, 'Topic_Label': True, 'Count': True},
                template='plotly_white')
fig_20.update_layout(xaxis_tickangle=-45) # rotate labels
# Save as interactive HTML
fig_20.write_html("../outputs/topic-modelling/visualization/top_20_topics_entire_dataset_yearly.html")
# save as csv
top_20.to_csv("../outputs/topic-modelling/exploration/top_20topics.csv")


#Top 10 Topics in Entire Dataset
# Get top 10 from previously computed top 20
top_10 = top_20.head(10)
# Check output
print(top_10)
# Create bar chart for top 10 topics
fig_10 = px.bar(top_10, 
                x='Topic_Label', y='Count',
                title='Top 10 Dominant Topics in Entire Dataset',
                labels={'Topic_Label': 'Topic'},
                hover_data={'Count': True, 'Topic_Label': True, 'Count': True},
                template='plotly_white')
# Rotate x-axis labels
fig_10.update_layout(xaxis_tickangle=-45)
# save chart as interactive HTML
fig_10.write_html("../outputs/topic-modelling/visualization/top_10_topics_entire_dataset_yearly.html")
# save as csv
top_10.to_csv("../outputs/topic-modelling/exploration/top_10topics.csv")

# Main Argument
# Top 5 Topic Trends After War Began (Oct 7, 2023)
# Which topics dominated since the start of War?

# Convert to datetime for filtering
df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
# Print and check
print(df['date'])
# Define start of war
war_start = pd.Timestamp("2023-10-07")
# Filter posts after war began
df_war = df[df['date'] >= war_start]
# Print and check
print(df_war)
# Create a new column with Month-Year format # For trend visualization 
df_war['Month'] = df_war['date'].dt.to_period('M').astype(str)

# Identify top 5 topics since war began
top_5_labels = df_war['Topic_Label'].value_counts().head(5).index.tolist()
# Print and check
print(top_5_labels)
# Filter dataset to keep only top 5 war-related topics
df_top5_war = df_war[df_war['Topic_Label'].isin(top_5_labels)]
# Check filtered war data
print(df_top5_war )
# Aggregate counts by month and topic (Group by Month and Topic_Label)
monthly_counts = df_top5_war.groupby(['Month', 'Topic_Label']).size().reset_index(name='Count')
print(monthly_counts)
# Create interactive bar chart showing topic trends over time
fig_trend = px.bar(monthly_counts,
                   x='Month',
                   y='Count',
                   color='Topic_Label',
                   title='Monthly Trend of Top 5 Dominant Topics During War (Post 7 Oct 2023)',
                   labels={'Topic_Label': 'Topic', 'Count': 'Mentions'},
                   hover_data={'Month': True, 'Topic_Label': True, 'Count': True},
                   template='plotly_white')
# group bars and rotate labels
fig_trend.update_layout(barmode='group', xaxis_tickangle=-45)
# save chart as interactive HTML
fig_trend.write_html("../outputs/topic-modelling/visualization/top_5_topics_war_period_monthly_trend.html")
# Display
fig_trend.show()
# save as csv
monthly_counts.to_csv("../outputs/topic-modelling/exploration/monthly_counts.csv")
