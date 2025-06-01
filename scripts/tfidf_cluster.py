import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/dataframes/tfidf/tfidf-over-0.3.csv")
print("Available columns:", df.columns.tolist())

df = df.dropna(subset=['year-1', 'month-1', 'day-1'])

df['year-1'] = pd.to_numeric(df['year-1'], errors='coerce').astype('Int64')
df['month-1'] = pd.to_numeric(df['month-1'], errors='coerce').astype('Int64')
df['day-1'] = pd.to_numeric(df['day-1'], errors='coerce').astype('Int64')


df = df.dropna(subset=['year-1', 'month-1', 'day-1'])

# Construct datetime from renamed columns
df['date-1'] = pd.to_datetime(
    df[['year-1', 'month-1', 'day-1']].rename(
        columns={'year-1': 'year', 'month-1': 'month', 'day-1': 'day'}
    ),
    errors='coerce'
)


df['month'] = df['date-1'].dt.strftime('%B')
df['month'] = pd.Categorical(df['month'], categories=[
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
], ordered=True)


threshold = df['similarity'].quantile(0.95)
df = df[df['similarity'] >= threshold]

print("Top 5% similarity pairs:")
print(df[['filename-1', 'filename-2', 'similarity']])

keywords = ['hospital', 'medical', 'surgeon', 'drone', 'missile', 'strike']
df_theme = df[
    df['title-1'].str.contains('|'.join(keywords), case=False, na=False) |
    df['title-2'].str.contains('|'.join(keywords), case=False, na=False)
]
df_theme.to_csv("C:/Users/HP/Downloads/FASDH25-portfolio3/outputs/tfidf_theme_filtered.csv", index=False)


edges = df[['filename-1', 'filename-2', 'similarity']].rename(
    columns={'filename-1': 'Source', 'filename-2': 'Target', 'similarity': 'Weight'}
)
edges.to_csv("C:/Users/HP/Downloads/FASDH25-portfolio3/outputs/tfidf_edges.csv", index=False)

nodes = pd.concat([
    df[['filename-1', 'title-1']].rename(columns={'filename-1': 'Id', 'title-1': 'Label'}),
    df[['filename-2', 'title-2']].rename(columns={'filename-2': 'Id', 'title-2': 'Label'})
]).drop_duplicates()
nodes.to_csv("C:/Users/HP/Downloads/FASDH25-portfolio3/outputs/tfidf_nodes.csv", index=False)

fig = px.scatter(
    df,
    x='month',
    y='similarity',
    color='year-1',
    title='Top 5% Article Similarity Clusters by Month',
    hover_data=['title-1', 'title-2']
)

fig.update_layout(
    xaxis_title='Month of Publication',
    yaxis_title='TF-IDF Cosine Similarity',
    legend_title='Publication Year',
    template='plotly_white'
)

fig.write_image("C:/Users/HP/Downloads/FASDH25-portfolio3/outputs/tfidf_clusters.png")
fig.write_html("C:/Users/HP/Downloads/FASDH25-portfolio3/outputs/tfidf_clusters.html")
