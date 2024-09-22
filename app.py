import streamlit as st
import pandas as pd
import umap_impl
import numpy as np

# st.set_page_config(layout="wide")
st.title("Map2 App")
st.write("Created as a part of Sundai Hack on 22nd September 2024")

#Define the 2 columns, chat on left and the graph on right
# col1, col2 = st.columns([4,6], gap='large')

with open('d3-test-code.html', 'r') as file:
    html_code = file.read()

html_code = html_code.split('//@#$%^')
assert(len(html_code)==3)
data_string = """
      {x: 10, y: 20, size: 5, z: 3, w: 2},
      {x: 20, y: 34, size: 8, z: 7, w: 1},
      {x: 35, y: 45, size: 3, z: 2, w: 2},
      {x: 45, y: 67, size: 7, z: 9, w: 2},
      {x: 55, y: 78, size: 4, z: 5, w: 1},
      {x: 60, y: 90, size: 6, z: 1, w: 2},
      {x: 75, y: 80, size: 9, z: 8, w: 2},
      {x: 85, y: 100, size: 2, z: 4, w: 2},
"""

# st.markdown(
#     html_code, 
# unsafe_allow_html=True
# )

# st.header("Altair Chart")

# df = pd.DataFrame({
#     'UMAP1': [1, 2, 3, 4, 5],
#     'UMAP2': [5, 4, 3, 2, 1],
#     'label': ['A', 'B', 'C', 'D', 'E']
# })

# chart = alt.Chart(df).mark_circle(size=60).encode(
#     x='UMAP1',
#     y='UMAP2',
#     tooltip=['label']
# ).interactive()

# st.altair_chart(chart, use_container_width=True)


# st.header("Plotly Chart")

# import plotly.express as px

# # Create a DataFrame with UMAP results
# df = pd.DataFrame({
#     'UMAP1': [1, 2, 3, 4, 5],
#     'UMAP2': [5, 4, 3, 2, 1],
#     'label': ['A', 'B', 'C', 'D', 'E']
# })

# fig = px.scatter(df, x='UMAP1', y='UMAP2', text='label')
# st.plotly_chart(fig)

def retrieve_embeddings(file_path):
    f2d_embedding = np.load(file_path)
    return f2d_embedding

embedding = retrieve_embeddings('yc_f2d_embedding.npy')

# Parse through and print x & y coordinates of embedding
data_string = ""
for point in embedding:
    x, y = point[0], point[1]
    data_string = data_string + f"{{x: {x}, y: {y}, size: 5, z: 3, w: 2}},\n"


st.components.v1.html(html_code[0]+data_string+html_code[2], height=800)