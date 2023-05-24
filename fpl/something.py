import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Define the data for the first table
table1_data = {'Name': ['John', 'Alice', 'Bob', 'Emily', 'David', 'Linda', 'Tom'],
               'Points': [10, 20, 30, 40, 50, 60, 70]}

# Define the data for the second table
table2_data = {'Name': ['John', 'Alice', 'Bob', 'Emily', 'David', 'Linda', 'Tom'],
               'Points': [5, 15, 25, 35, 45, 55, 65]}

# Create dataframes for the two tables
df1 = pd.DataFrame(table1_data)
df2 = pd.DataFrame(table2_data)

# Calculate the difference in points between the two tables
df_diff = df2.copy()
df_diff['Points'] = df2['Points'] - df1['Points']

# Create a line plot to represent the change in points
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df_diff['Name'],
    y=df_diff['Points'],
    mode='lines+markers',
    line=dict(color='blue'),
    marker=dict(color='blue', size=10),
    name='Point Difference'
))

fig.update_layout(
    title='Change in Points between Tables',
    xaxis=dict(title='Name'),
    yaxis=dict(title='Point Difference')
)

# Display the chart in Streamlit
st.plotly_chart(fig)