# Import necessary libraries
import pandas as pd
import plotly.express as px
import plotly.io as pio
import os

# Print the current working directory for debugging
print("Current working directory:", os.getcwd())

# Define data path
data_dir = "../data/dataframes/tfidf/"
file_path = data_dir + "tfidf-over-0.3.csv"

try:
    print(f"Contents of expected data directory: {data_dir}")
    if os.path.exists(data_dir):
        print(os.listdir(data_dir))
    else:
        print(f"Error: The directory {data_dir} was not found.")
except FileNotFoundError:
    print(f"Error accessing directory {data_dir}. Please check the path.")

df = None  # Initialize df

# Load the dataset
try:
    df = pd.read_csv(file_path)
    print("File loaded successfully.")
except FileNotFoundError:
    print(f"Error: The file {file_path} was not found.")

# Proceed if dataframe is loaded
if df is not None:
    print("Available columns:", df.columns.tolist())

    # Ensure required date columns exist
    required_date_cols = ['year-1', 'month-1', 'day-1']
    if all(col in df.columns for col in required_date_cols):
        df = df.dropna(subset=required_date_cols)

        df['year-1'] = pd.to_numeric(df['year-1'], errors='coerce').astype('Int64')
        df['month-1'] = pd.to_numeric(df['month-1'], errors='coerce').astype('Int64')
        df['day-1'] = pd.to_numeric(df['day-1'], errors='coerce').astype('Int64')

        df = df.dropna(subset=required_date_cols)

        # Rename for datetime construction
        date_cols_renamed = df[required_date_cols].rename(columns={
            'year-1': 'year', 'month-1': 'month', 'day-1': 'day'
        })
        df['date-1'] = pd.to_datetime(date_cols_renamed, errors='coerce')
        df = df.dropna(subset=['date-1'])

        df = df.copy()  # Avoid SettingWithCopyWarning
        df['month_start'] = df['date-1'].dt.to_period('M').dt.to_timestamp()

        df['month'] = df['date-1'].dt.strftime('%B')
        df['month'] = pd.Categorical(df['month'], categories=[
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ], ordered=True)

        # Filter by similarity threshold
        if 'similarity' in df.columns:
            threshold = df['similarity'].quantile(0.95)
            df = df[df['similarity'] >= threshold]

            print("Top 5% similarity pairs:")
            if all(col in df.columns for col in ['filename-1', 'filename-2', 'similarity']):
                print(df[['filename-1', 'filename-2', 'similarity']])
            else:
                print("Required columns for similarity pairs not found.")
        else:
            print("Column 'similarity' not found. Skipping similarity filtering.")

        # Filter by keywords in titles
        keywords = ['hospital', 'medical', 'surgeon', 'drone', 'missile', 'strike']
        if 'title-1' in df.columns and 'title-2' in df.columns:
            df_theme = df[
                df['title-1'].str.contains('|'.join(keywords), case=False, na=False) |
                df['title-2'].str.contains('|'.join(keywords), case=False, na=False)
            ]
            os.makedirs("outputs", exist_ok=True)
            df_theme.to_csv("outputs/tfidf_theme_filtered.csv", index=False)
            print("Theme-filtered data saved to outputs/tfidf_theme_filtered.csv")
        else:
            print("Columns 'title-1' or 'title-2' not found. Skipping theme filtering.")

        # Prepare edges
        if all(col in df.columns for col in ['filename-1', 'filename-2', 'similarity']):
            edges = df[['filename-1', 'filename-2', 'similarity']].rename(
                columns={'filename-1': 'Source', 'filename-2': 'Target', 'similarity': 'Weight'}
            )
            os.makedirs("outputs", exist_ok=True)
            edges.to_csv("outputs/tfidf_edges.csv", index=False)
            print("Edges data saved to outputs/tfidf_edges.csv")
        else:
            print("Required columns for edges not found.")

        # Prepare nodes
        if all(col in df.columns for col in ['filename-1', 'title-1', 'filename-2', 'title-2']):
            nodes = pd.concat([
                df[['filename-1', 'title-1']].rename(columns={'filename-1': 'Id', 'title-1': 'Label'}),
                df[['filename-2', 'title-2']].rename(columns={'filename-2': 'Id', 'title-2': 'Label'})
            ]).drop_duplicates()
            os.makedirs("outputs", exist_ok=True)
            nodes.to_csv("outputs/tfidf_nodes.csv", index=False)
            print("Nodes data saved to outputs/tfidf_nodes.csv")
        else:
            print("Required columns for nodes not found.")

        start_date = pd.Timestamp("2023-10-01")
        end_date = pd.Timestamp("2024-04-30")
        df = df[(df['date-1'] >= start_date) & (df['date-1'] <= end_date)]




        # Plot
        if all(col in df.columns for col in ['month', 'similarity', 'year-1', 'title-1', 'title-2']):
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

            os.makedirs("outputs", exist_ok=True)
            fig.write_image("outputs/tfidf_clusters.png")
            print("Plot saved as outputs/tfidf_clusters.png")
            fig.write_html("outputs/tfidf_clusters.html")
            print("Plot saved as outputs/tfidf_clusters.html")
        else:
            print("Required columns for plotting not found.")
    else:
        print("Required date columns not found in dataframe.")
else:
    print("Dataframe not loaded. Skipping processing.")
