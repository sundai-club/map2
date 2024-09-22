import numpy as np

def load_embeddings(file_path):
    f2d_embedding = np.load(file_path)
    return f2d_embedding

if __name__ == '__main__':
    load_embeddings('yc_f2d_embedding.npy')