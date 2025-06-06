import pandas as pd
import plotly.express as px
import plotly.io as pio
import os

# Define war start date
war_start_date = pd.Timestamp("2023-10-07")

# Print current working directory for debugging
print("Current working directory:", os.getcwd())

# Define data path
data_dir = "../data/dataframes/tfidf/"

#Code take from FASDH-14.2 slide
file_path = data_dir + "tfidf-over-0.3.csv"

try:
    print(f"Contents of expected data directory: {data_dir}")
    if os.path.exists(data_dir):
        print(os.listdir(data_dir))
    else:
        print(f"Error: The directory {data_dir} was not found.")
except FileNotFoundError:
    print(f"Error accessing directory {data_dir}. Please check the path.")

df = None

# Load the dataset
try:
    df = pd.read_csv(file_path)
    print("File loaded successfully.")
except FileNotFoundError:
    print(f"Error: The file {file_path} was not found.")

if df is not None:
    print("Available columns:", df.columns.tolist())

    required_date_cols = ['year-1', 'month-1', 'day-1']
    if all(col in df.columns for col in required_date_cols):
        df = df.dropna(subset=required_date_cols)

        df['year-1'] = pd.to_numeric(df['year-1'], errors='coerce').astype('Int64')
        df['month-1'] = pd.to_numeric(df['month-1'], errors='coerce').astype('Int64')
        df['day-1'] = pd.to_numeric(df['day-1'], errors='coerce').astype('Int64')

        df = df.dropna(subset=required_date_cols)

        date_cols_renamed = df[required_date_cols].rename(columns={
            'year-1': 'year', 'month-1': 'month', 'day-1': 'day'
        })

        df['date-1'] = pd.to_datetime(date_cols_renamed, errors='coerce')
        df = df.dropna(subset=['date-1'])

        df['month_start'] = df['date-1'].dt.to_period('M').dt.to_timestamp()

        month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December']
        df['month'] = df['date-1'].dt.strftime('%B')
        df['month'] = pd.Categorical(df['month'], categories=month_order, ordered=True)

        df['war_time'] = df['date-1'] >= war_start_date

        if 'similarity' in df.columns:
            threshold = df['similarity'].quantile(0.95)
            df = df[df['similarity'] >= threshold]

            print("Top 5% similarity pairs:")
            if all(col in df.columns for col in ['filename-1', 'filename-2', 'similarity']):
                print(df[['filename-1', 'filename-2', 'similarity']])
            else:
                print("Required columns for similarity pairs not found.")

        keywords = ['hospital', 'medical', 'surgeon', 'drone', 'missile', 'strike']
        if 'title-1' in df.columns and 'title-2' in df.columns:
            df_theme = df[
                df['title-1'].str.contains('|'.join(keywords), case=False, na=False) |
                df['title-2'].str.contains('|'.join(keywords), case=False, na=False)
            ]
            os.makedirs("outputs", exist_ok=True)
            df_theme.to_csv("outputs/tfidf_theme_filtered.csv", index=False)
            print("Theme-filtered data saved.")
        else:
            print("Title columns not found. Skipping theme filtering.")

        if all(col in df.columns for col in ['filename-1', 'filename-2', 'similarity']):
            edges = df[['filename-1', 'filename-2', 'similarity']].rename(
                columns={'filename-1': 'Source', 'filename-2': 'Target', 'similarity': 'Weight'}
            )
            edges.to_csv("outputs/tfidf_edges.csv", index=False)
            print("Edges data saved.")

        if all(col in df.columns for col in ['filename-1', 'title-1', 'month-1', 'filename-2', 'title-2', 'month-2']):
            nodes = pd.concat([
                df[['filename-1', 'title-1', 'month-1']].rename(columns={
                    'filename-1': 'Id', 'title-1': 'Label', 'month-1': 'month'}),
                df[['filename-2', 'title-2', 'month-2']].rename(columns={
                    'filename-2': 'Id', 'title-2': 'Label', 'month-2': 'month'})
            ]).drop_duplicates()
            nodes.to_csv("outputs/tfidf_nodes.csv", index=False)
            print("Nodes data saved.")

        if all(col in df.columns for col in ['month_start', 'similarity', 'year-1', 'title-1', 'title-2']):
            fig_all = px.scatter(
                df,
                x='month_start',
                y='similarity',
                color='year-1',
                title='Top 5% Article Similarity Clusters by Month (All)',
                hover_data=['title-1', 'title-2']
            )
            fig_all.update_layout(xaxis_title='Month (Year)', yaxis_title='Similarity')
            fig_all.write_html("outputs/tfidf_clusters_all.html")
            print("Overall plot saved.")

            df_prewar = df[df['war_time'] == False].copy()
            fig_prewar = px.scatter(
                df_prewar,
                x='month_start',
                y='similarity',
                color='year-1',
                title='Article Similarity (Pre-War)',
                hover_data=['title-1', 'title-2']
            )
            fig_prewar.update_layout(xaxis_title='Month (Year)', yaxis_title='Similarity')
            fig_prewar.write_html("outputs/tfidf_clusters_prewar.html")
            print("Pre-war plot saved.")

            df_wartime = df[df['war_time'] == True].copy()
            fig_wartime = px.scatter(
                df_wartime,
                x='month_start',
                y='similarity',
                color='year-1',
                title='Article Similarity (During War)',
                hover_data=['title-1', 'title-2']
            )
            fig_wartime.update_layout(xaxis_title='Month (Year)', yaxis_title='Similarity')
            fig_wartime.write_html("outputs/tfidf_clusters_wartime.html")
            print("War-time plot saved.")
        else:
            print("Required columns for plotting not found.")
    else:
        print("Required date columns not found.")
else:
    print("Dataframe not loaded. Skipping processing.")
