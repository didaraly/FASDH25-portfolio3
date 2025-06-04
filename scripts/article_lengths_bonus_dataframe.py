# Import libraries
import pandas as pd
import plotly.express as px
import os

# Show current working directory (for debugging)
print("Current working directory:", os.getcwd())

data_dir = "./data/dataframes/lengths/"

file_path = os.path.join(data_dir, "article_lengths_by_month.csv")

# Try to load the data
try:
    df = pd.read_csv(file_path)
    print("Data loaded successfully.")
except FileNotFoundError:
    print(f"File not found: {file_path}")
    df = None

# Continue if data is loaded
if df is not None:
    print("Columns in dataset:", df.columns.tolist())

    # Check required columns
    if all(col in df.columns for col in ['year', 'month', 'avg_length']):
        # Remove rows with missing year or month
        df = df.dropna(subset=['year', 'month'])

        # Make sure year and month are numbers
        df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')
        df['month'] = pd.to_numeric(df['month'], errors='coerce').astype('Int64')

        # Create a date column from year and month (set day to 1)
        df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1), errors='coerce')

        # Filter to only include articles from Oct to Jan (across two years)
        start_date = pd.to_datetime("2023-10-01")
        end_date = pd.to_datetime("2024-01-31")
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

        # Optional: round average length for cleaner visuals
        df['avg_length'] = df['avg_length'].round(1)

        # Create a bar chart of average article length over time
        fig = px.bar(
            df,
            x='date',
            y='avg_length',
            color='year',
            title='Average Article Length (Oct 2023 to Jan 2024)',
            labels={'avg_length': 'Average Length (words)', 'date': 'Month'},
            text='avg_length'
        )

        # Clean up the plot layout
        fig.update_layout(
            template='plotly_white',
            xaxis_tickformat='%b %Y',
            xaxis_title='Month',
            yaxis_title='Average Length (words)'
        )

        # Save the plot
        os.makedirs("outputs", exist_ok=True)
        fig.write_image("outputs/article_lengths_oct_to_jan.png")
        fig.write_html("outputs/article_lengths_oct_to_jan.html")
        print("Plot saved to outputs folder.")
    else:
        print("Required columns ('year', 'month', 'avg_length') not found.")
else:
    print("No data to process.")
