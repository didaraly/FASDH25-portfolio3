#Which topics dominated coverage in 2023, and how do they compare to 2024?
# Import import libraries
import pandas as pd  
import plotly.express as px  

# Load data and clean topics  
df = pd.read_csv("../data/dataframes/topic-model/topic-model.csv")  
df = df[df['Topic'] != -1]  # Remove noise  
df['Topic_Label'] = df['topic_1'] + ', ' + df['topic_2']  

# Top topics in 2023 vs. 2024  
df_2023 = df[df['year'] == 2023]['Topic_Label'].value_counts().reset_index(name='2023')  
df_2024 = df[df['year'] == 2024]['Topic_Label'].value_counts().reset_index(name='2024')  
combined = pd.merge(df_2023, df_2024, on='Topic_Label', how='outer').fillna(0)  

# Diverging bar chart  
fig = px.bar(combined, x='Topic_Label', y=['2023', '2024'],  
             title='Topic Dominance: 2023 vs. 2024',  
             labels={'Topic_Label': 'Topic', 'value': 'Frequency'},  
             barmode='group')  
fig.update_layout(xaxis_tickangle=-45)  
fig.write_image("../outputs/topic_dominance.png")  
