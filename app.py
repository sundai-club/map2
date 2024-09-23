import streamlit as st
import pandas as pd
import umap
import numpy as np

from sentence_transformers import SentenceTransformer
# from scipy.spatial import distance
import math
# import pyperclip

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

def calculate_percentile(value, sorted_values):
    return np.searchsorted(sorted_values, value, side='left') / len(sorted_values) * 100


# # st.set_page_config(layout="wide")
# st.title("Map2 App")
# st.write("Created as a part of Sundai Hack on 22nd September 2024")


st.title("ProductViz: Uncover Product Hunt Trends")
st.write("Created as part of Sundai Hack on 22nd September 2024")

# Added new markdown content
st.markdown("""
## The Problem: Information Overload in Product Discovery

In today's fast-paced tech world, staying on top of new products and innovations is challenging. Product Hunt lists thousands of products, but making sense of this vast amount of information can be overwhelming. How can we quickly identify trends, spot unique offerings, and understand the product landscape?

## Our Solution: ProductViz

ProductViz is a powerful visualization tool that transforms Product Hunt data into an interactive, insightful experience. By leveraging advanced algorithms and intuitive design, we help you:

1. **Visualize the Product Landscape**: Our interactive graph plots products based on their attributes, allowing you to see clusters and patterns at a glance.
2. **Discover Trends**: Easily identify popular categories, emerging technologies, and market gaps.
3. **Find Similar Products**: Our UMAP grouping algorithm brings similar products closer together, making it easy to explore alternatives and competitors.
4. **Deep Dive into Details**: Click on any product to reveal its full attributes, upvotes, and more.

Explore the vast world of products with ease, and gain insights that can drive your next big idea or investment!
""")


#Define the 2 columns, chat on left and the graph on right
# col1, col2 = st.columns([4,6], gap='large')

with open('d3-test-code.html', 'r') as file:
    html_code = file.read()

html_code = html_code.split('//@#$%^')
assert(len(html_code)==3)


def retrieve_embeddings(file_path):
    f2d_embedding = np.load(file_path)
    return f2d_embedding

data = pd.read_csv('producthunt_f2d_embedding.csv')
embedding = data.values
emb = embedding[:,-2:]

# Parse through and print x & y coordinates of embedding
data_string = ""

# Create a sorted list of different 'topic_slugs' with their respective frequencies
topic_slugs = data['topic_slug'].str.split(',', expand=True).stack()
topic_slug_counts = topic_slugs.value_counts()
sorted_topic_slugs = topic_slug_counts.sort_values(ascending=False)
# Create a dictionary of top 7 topic slugs with their ranks
top_7_slugs = {slug: rank + 1 for rank, slug in enumerate(sorted_topic_slugs.head(7).index)}

for i in range(len(embedding)):
            # st.write(embedding[i][22], embedding[i][23])
    dd = embedding[i]
    # st.write(embedding)
    x, y = dd[26], dd[27]

            # {x: 20, y: 34, size: 8, z: 7, w: 1, name: "abe", traction: 24, tagline: "Simplify your workflow", age: "3 years", category: "Fintech"},
    # st.write(embedding[i])
    # st.write(dd[14])
    if type(dd[14]) != str:
        # st.write(dd[14])
        dd[14] = ""
    size = int(dd[25]/100.0 * 20)  # Scale traction_rank to size (1-20)
    z = min(int(dd[23] * 9) + 1, 9)  # Scale age_rank to z (1-9)
    w = top_7_slugs.get(dd[14],7)

    data_string += f"{{x: {x}, y: {y}, size: {size}, z: {z}, w: {w}, "
    data_string += f"name: \"{dd[2]}\", traction: {data['traction'][i]}, "
    data_string += f"tagline: \"{dd[4]}\", age: \"{data['age'][i]} days\", "
    data_string += f"category: \"{dd[14].split(',')[0]}\"}},"
    # if i != (len(embedding)):
    #     data_string += ",\n"

# st.write(data_string)
html_code2 = html_code[0] + data_string + html_code[2]
# pyperclip.copy(html_code2)

st.components.v1.html(html_code2, height=800)


# st.write(emb)

# # # Plot the 2D embeddings
# plt.figure(figsize=(10, 8))
# plt.scatter(f2d_embedding[:, 0], f2d_embedding[:, 1], s=5, cmap='Spectral')
# plt.title('UMAP projection of the embeddings')
# plt.xlabel('UMAP 1')
# plt.ylabel('UMAP 2')
# plt.colorbar()
# plt.show()

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
        dd = points_to_display[i]
        x, y = dd[26], dd[27]

                # {x: 20, y: 34, size: 8, z: 7, w: 1, name: "abe", traction: 24, tagline: "Simplify your workflow", age: "3 years", category: "Fintech"},

        size = int(dd[25]/100.0 * 20)  # Scale traction_rank to size (1-20)
        z = min(int(dd[23] * 9) + 1, 9)  # Scale age_rank to z (1-9)
        w = top_7_slugs.get(dd[14],7)

        data_string += f"{{x: {x}, y: {y}, size: {size}, z: {z}, w: {w}, "
        data_string += f"name: \"{dd[2]}\", traction: {data['traction'][i]}, "
        data_string += f"tagline: \"{dd[4]}\", age: \"{data['age'][i]} days\", "
        data_string += f"category: \"{dd[14].split(',')[0]}\"}},\n"

    st.components.v1.html(html_code[0] + data_string + html_code[2], height=800)

# Added more content about why ProductViz matters
st.markdown("""
## Why ProductViz Matters

In an era of rapid innovation, ProductViz serves as your compass in the vast sea of new products and startups. Whether you're an entrepreneur, investor, or tech enthusiast, our tool empowers you to:

- **Stay Ahead of the Curve**: Identify emerging trends before they become mainstream.
- **Find Your Niche**: Discover gaps in the market that your next big idea could fill.
- **Competitive Analysis**: Understand how your product or idea fits into the existing landscape.
- **Inspiration**: Get inspired by innovative products across various categories.

By visualizing the Product Hunt ecosystem, we're not just showing you data – we're revealing opportunities.
""")

# Footer
st.markdown("---")
st.write("© 2024 ProductViz | Data sourced from Product Hunt")

