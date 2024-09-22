import streamlit as st
import altair as alt
import pandas as pd

# st.set_page_config(layout="wide")
st.title("Map2 App")
st.write("Created as a part of Sundai Hack on 22nd September 2024")

#Define the 2 columns, chat on left and the graph on right
# col1, col2 = st.columns([4,6], gap='large')

with open('/Users/anushkasingh/Desktop/Code/hobby-projects/map2/d3-test-code.html', 'r') as file:
    html_code = file.read()

st.components.v1.html(html_code, height=600)

# st.markdown(
#     html_code, 
# unsafe_allow_html=True
# )

st.header("Altair Chart")

df = pd.DataFrame({
    'UMAP1': [1, 2, 3, 4, 5],
    'UMAP2': [5, 4, 3, 2, 1],
    'label': ['A', 'B', 'C', 'D', 'E']
})

chart = alt.Chart(df).mark_circle(size=60).encode(
    x='UMAP1',
    y='UMAP2',
    tooltip=['label']
).interactive()

st.altair_chart(chart, use_container_width=True)

st.header("Bokeh Chart")

from bokeh.plotting import figure
from bokeh.io import output_file, save

df = pd.DataFrame({
    'UMAP1': [1, 2, 3, 4, 5],
    'UMAP2': [5, 4, 3, 2, 1],
    'label': ['A', 'B', 'C', 'D', 'E']
})

p = figure(title="UMAP Scatter Plot", tools="hover", tooltips="@label")
p.circle(x='UMAP1', y='UMAP2', source=df, size=10)

st.bokeh_chart(p)

st.header("Plotly Chart")

import plotly.express as px

# Create a DataFrame with UMAP results
df = pd.DataFrame({
    'UMAP1': [1, 2, 3, 4, 5],
    'UMAP2': [5, 4, 3, 2, 1],
    'label': ['A', 'B', 'C', 'D', 'E']
})

fig = px.scatter(df, x='UMAP1', y='UMAP2', text='label')
st.plotly_chart(fig)