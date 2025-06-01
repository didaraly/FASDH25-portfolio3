# Import libraries
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("../data/dataframes/topic-model/topic-model.csv")


# Initial Cleaning
# Remove noise topic -1
df = df[df['Topic'] != -1].copy()
print(df)
# List of common English stop words copied from NLTK's list of english stopwords:
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
    "very", "s", "to", "can", "will", "just", "don", "should", "now"]

# Filter out rows where either topic_1 or topic_2 is a stopword
df = df[~df['topic_1'].str.lower().isin(stop_words)]
df = df[~df['topic_2'].str.lower().isin(stop_words)]
df = df[~df['topic_3'].str.lower().isin(stop_words)]
df = df[~df['topic_4'].str.lower().isin(stop_words)]
# Create a combined topic label
df['Topic_Label'] = df['topic_1'] + ', ' + df['topic_2'] + ',' + df['topic_3'] + ',' + df['topic_4']

# Top 20 Dominant Topics Overall
top_20 = df['Topic_Label'].value_counts().head(20).reset_index()
print(top_20)
top_20.columns = ['Topic_Label', 'Count']
print(top_20.columns)
fig_20 = px.bar(top_20, 
                x='Topic_Label', y='Count',
                title='Top 20 Dominant Topics in Entire Dataset',
                labels={'Topic_Label': 'Topic'},
                template='plotly_white')
fig_20.update_layout(xaxis_tickangle=-45)
fig_20.write_html("../outputs/top_20_topics.html")

# Top 10 Dominant Topics Overall
top_10 = top_20.head(10)
print(top_10)
fig_10 = px.bar(top_10, 
                x='Topic_Label', y='Count',
                title='Top 10 Dominant Topics in Entire Dataset',
                labels={'Topic_Label': 'Topic'},
                template='plotly_white')
fig_10.update_layout(xaxis_tickangle=-45)
fig_10.write_html("../outputs/top_10_topics.html")

# Top 5 Topics During War (After 7 Oct 2023)
# Convert to datetime
df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
war_start = pd.Timestamp("2023-10-07")
df_war = df[df['date'] >= war_start].copy()

# Format month-year for trend visualization
df_war['Month'] = df_war['date'].dt.to_period('M').astype(str)

# Get top 5 topics during war period
top_5_labels = df_war['Topic_Label'].value_counts().head(5).index.tolist()
df_top5_war = df_war[df_war['Topic_Label'].isin(top_5_labels)]
print(df_top5_war )
# Group by Month and Topic_Label
monthly_counts = df_top5_war.groupby(['Month', 'Topic_Label']).size().reset_index(name='Count')

# Plot interactive bar chart
fig_trend = px.bar(monthly_counts,
                   x='Month',
                   y='Count',
                   color='Topic_Label',
                   title='Monthly Trend of Top 5 Dominant Topics During War (Post 7 Oct 2023)',
                   labels={'Topic_Label': 'Topic', 'Count': 'Mentions'},
                   hover_data={'Month': True, 'Topic_Label': True, 'Count': True},
                   template='plotly_white')

fig_trend.update_layout(barmode='group', xaxis_tickangle=-45)
fig_trend.write_html("../outputs/top_5_war_monthly_trend.html")
fig_trend.show()
