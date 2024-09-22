import umap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Sample data: Replace this with your actual data loading
data = {
    'feature1': np.random.rand(100),
    'feature2': np.random.rand(100),
    'feature3': np.random.rand(100),
    'feature4': np.random.rand(100)
}
df = pd.DataFrame(data)

# Initialize UMAP model
reducer = umap.UMAP()

# Fit and transform the data
embedding = reducer.fit_transform(df)

# Plot the results
plt.scatter(embedding[:, 0], embedding[:, 1])
plt.title('UMAP projection of custom pandas DataFrame')
plt.xlabel('UMAP1')
plt.ylabel('UMAP2')
plt.show()