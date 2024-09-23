import streamlit as st
import pandas as pd
import numpy as np
from scipy.spatial import distance

# Keep external file references
embedding = pd.read_csv('producthunt_f2d_embedding.csv').values
emb = embedding[:, :-2]

with open('d3-test-code.html', 'r') as file:
    html_code = file.read()
html_code = html_code.split('//@#$%^')
assert(len(html_code)==3)

st.set_page_config(layout="wide", page_title="ProductViz: Discover Product Hunt Trends")

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

# Added sidebar for filters and search
st.sidebar.header("Explore Products")
search_query = st.sidebar.text_input("Search products")
category_filter = st.sidebar.multiselect("Filter by category", ["Tech", "Productivity", "Design", "Marketing", "AI"])
date_range = st.sidebar.date_input("Launch date range", [])

# Main visualization and logic
def calculate_distance(q_embedding, emb):
    distances = [distance.euclidean(q_embedding, emb) for emb in embedding]
    closest_indices = np.argsort(distances)[:100]
    closest_points = embedding[closest_indices]
    return closest_points

with st.form(key='query_form'):
    name = st.text_input('Enter your Query')
    submit_button = st.form_submit_button(label='Submit')

while True:
    if name:
        st.write(f"Query: {name}")
        # Implement query logic here
    else:
        # Default visualization logic
        data_string = ""
        for i in range(len(embedding)):
            x, y = embedding[i][22], embedding[i][23]
            data_string = data_string + f"{{x: {x}, y: {y}, size: 5, z: 3, w: 2}},\n"
        st.components.v1.html(html_code[0]+data_string+html_code[2], height=800)

    if submit_button == False:
        break

# Added placeholder for search results or filtered view
if search_query or category_filter or date_range:
    st.subheader("Search Results")
    st.write("Displaying results based on your filters (placeholder)")
    # Here you would implement the actual search and filtering logic
else:
    st.subheader("How to Use ProductViz")
    st.write("""
    1. Use the sidebar to search for specific products or filter by category and launch date.
    2. Explore the interactive visualization to see product clusters and relationships.
    3. Click on any point in the visualization to view detailed product information.
    4. Discover trends and insights in the product landscape to inform your decisions.
    """)

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

