import streamlit as st
import altair as alt
import pandas as pd

# st.set_page_config(layout="wide")
st.title("Map2 App")
st.write("Created as a part of Sundai Hack on 22nd September 2024")

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