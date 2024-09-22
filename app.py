import streamlit as st
import pandas as pd
# import umap_impl
import numpy as np

# from sentence_transformers import SentenceTransformer
from scipy.spatial import distance

# def convert_to_embeddings(text):
#     # Load the Sentence Transformer model
#     model = SentenceTransformer('all-mpnet-base-v2')

#     # Encode the texts
#     embedding = model.encode(text)

#     return embedding

def calculate_distance(q_embedding, emb):
    # Calculate distances from q_embedding to all points in embedding
    distances = [distance.euclidean(q_embedding, emb) for emb in embedding]

    # Get indices of the 100 closest points
    closest_indices = np.argsort(distances)[:100]

    # Filter the embedding to get the 100 closest points
    closest_points = embedding[closest_indices]
    return closest_points

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
emb = embedding[:, :-2]

# st.write(emb)

with st.form(key='query_form'):
    name = st.text_input('Enter your Query')
    submit_button = st.form_submit_button(label='Submit')

while True:
    if name:
        st.write(f"Query: {name}")
        # q_embedding = convert_to_embeddings(name)

        # closest_points = calculate_distance(q_embedding, embedding)

        # Update data_string with the 100 closest points
        # data_string = ""
        # for point in closest_points:
        #     x, y = point[8], point[9]
        #     data_string += f"{{x: {x}, y: {y}, size: 5, z: 3, w: 2}},\n"

        # st.components.v1.html(html_code[0] + data_string + html_code[2], height=800)
    else:
        # Parse through and print x & y coordinates of embedding
        data_string = ""
        # st.write(embedding)
        # st.write(embedding.shape)

        for i in range(len(embedding)):
            # st.write(embedding[i][22], embedding[i][23])
            x, y = embedding[i][22], embedding[i][23]
            data_string = data_string + f"{{x: {x}, y: {y}, size: 5, z: 3, w: 2}},\n"

        st.components.v1.html(html_code[0]+data_string+html_code[2], height=800)

    if submit_button == False:
        break




