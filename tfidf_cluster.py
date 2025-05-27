
#Which articles form the densest similarity clusters, and what themes do they share?
import pandas as pd  
import plotly.express as px  

# Load data and filter top 5% similarities  
df = pd.read_csv("./data/dataframes/tfidf/tfidf-over-0.3.csv")  
df = df[df['similarity'] >= df['similarity'].quantile(0.95)]  
print(df)
# Prepare nodes and edges for Gephi
edges = df[['filename-1', 'filename-2', 'similarity']].rename(  
    columns={'filename-1': 'Source', 'filename-2': 'Target', 'similarity': 'Weight'})  
edges.to_csv("scripts/outputs/tfidf_edges.csv", index=False)  

# Extract nodes with titles  
nodes = pd.concat([  
    df[['filename-1', 'title-1']].rename(columns={'filename-1': 'Id', 'title-1': 'Label'}),  
    df[['filename-2', 'title-2']].rename(columns={'filename-2': 'Id', 'title-2': 'Label'})  
]).drop_duplicates()  
nodes.to_csv("./scripts/outputs/tfidf_nodes.csv", index=False)  

# Temporal cluster analysis
df['month'] = pd.to_datetime(df['day-1']).dt.month  
fig = px.scatter(df, x='month', y='similarity', color='year-1',  
                 title='Article Similarity Clusters by Month',  
                 hover_data=['title-1', 'title-2'])  
fig.write_image("scripts/outputs/tfidf_clusters.png")
fig.write_html("output.html")
