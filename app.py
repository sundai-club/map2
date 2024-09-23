import streamlit as st
import pandas as pd
import umap
import numpy as np

from sentence_transformers import SentenceTransformer
from scipy.spatial import distance
import math

def convert_to_embeddings(text):
    # Load the Sentence Transformer model
    model = SentenceTransformer('all-mpnet-base-v2')

    # Encode the texts
    embedding = model.encode([text])

    # Initialize UMAP model
    reducer = umap.UMAP(n_components=2, random_state=42)

    # Fit and transform the data
    f2d_embedding = reducer.fit_transform(embedding)

    return f2d_embedding

def calculate_distance(q_embedding, emb):
    # Calculate distances from q_embedding to all points in embedding
    st.write(q_embedding.shape)
    st.write(emb.shape)

    distances = [math.sqrt(((emb[0] - q_embedding[0][0]) ** 2) + ((emb[1] - q_embedding[0][1]) ** 2)) for emb in embedding]

    # Get indices of the 10 closest points
    emb = np.column_stack((emb, distances))
    emb = emb[emb[:, 2].argsort()]
    closest_indices = emb[:100, :2]
    # st.write(closest_indices)

    return closest_indices

# st.set_page_config(layout="wide")
st.title("Map2 App")
st.write("Created as a part of Sundai Hack on 22nd September 2024")

#Define the 2 columns, chat on left and the graph on right
# col1, col2 = st.columns([4,6], gap='large')

with open('d3-test-code.html', 'r') as file:
    html_code = file.read()

html_code = html_code.split('//@#$%^')
assert(len(html_code)==3)


def retrieve_embeddings(file_path):
    f2d_embedding = np.load(file_path)
    return f2d_embedding

embedding = pd.read_csv('producthunt_f2d_embedding.csv').values
emb = embedding[:,-2:]

# Parse through and print x & y coordinates of embedding
data_string = ""
        # st.write(embedding)
        # st.write(embedding.shape)

for i in range(len(embedding)):
            # st.write(embedding[i][22], embedding[i][23])
    x, y = embedding[i][22], embedding[i][23]
    data_string = data_string + f"{{x: {x}, y: {y}, size: 5, z: 3, w: 2}},\n"

st.components.v1.html(html_code[0]+data_string+html_code[2], height=800)

# st.write(emb)

with st.form(key='query_form'):
    name = st.text_input('Enter your Query')
    submit_button = st.form_submit_button(label='Submit')


if submit_button:
    st.subheader("Query Results")
    st.write(f"Query: {name}")
    st.empty()
    q_embedding = convert_to_embeddings(name)

    closest_points = calculate_distance(q_embedding, emb)
    points_to_display = []

    for i in range(len(closest_points)):
        for j in range(len(embedding)):
            if (closest_points[i] == embedding[j][-2:]).all():
                # st.write(embedding[j])
                points_to_display.append(embedding[j])

    data_string = ""
        # st.write(embedding)
        # st.write(embedding.shape)

    for i in range(len(points_to_display)):
        x, y = points_to_display[i][22], points_to_display[i][23]
        data_string = data_string + f"{{x: {x}, y: {y}, size: 5, z: 3, w: 2}},\n"

    st.components.v1.html(html_code[0] + data_string + html_code[2], height=800)




