import umap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer

def convert_to_embeddings(texts):
    # Load the Sentence Transformer model
    model = SentenceTransformer('all-mpnet-base-v2')

    # Encode the texts
    embeddings = model.encode(texts)

    return embeddings


def load_and_save_embeddings(file_path, save_file_name):
    # Load data from CSV file
    data = pd.read_csv(file_path)
    df = pd.DataFrame(data)

    print(df.head())

    texts = [" Company Name: " + str(df['Company'][i]) + " Description: " + str(df['Description'][i]) + " Sector: " + str(df['Sector'][i]) + " Location: " + str(df['Location'][i]) for i in range(len(df))]
    print(texts)
    print("\n\n")
    embeddings = convert_to_embeddings(texts)

    # Initialize UMAP model
    reducer = umap.UMAP(n_components=2, random_state=42)

    # Fit and transform the data
    f2d_embedding = reducer.fit_transform(embeddings)

    print("\n\nEmbeddings shape:", f2d_embedding.shape)
    print("\n\nEmbedding Type:", type(f2d_embedding))

    np.save(save_file_name, f2d_embedding)
    # f2d_embedding = np.load('f2d_embedding.npy')

# # Plot the 2D embeddings
# plt.figure(figsize=(10, 8))
# plt.scatter(f2d_embedding[:, 0], f2d_embedding[:, 1], s=5, cmap='Spectral')
# plt.title('UMAP projection of the embeddings')
# plt.xlabel('UMAP 1')
# plt.ylabel('UMAP 2')
# plt.colorbar()
# plt.show()

def retrieve_embeddings(file_path):
    f2d_embedding = np.load(file_path)
    return f2d_embedding

if __name__ == '__main__':
    load_and_save_embeddings('/Users/anushkasingh/Desktop/Code/hobby-projects/map2/2023-02-27-yc-companies.csv', 'yc_f2d_embedding.npy')