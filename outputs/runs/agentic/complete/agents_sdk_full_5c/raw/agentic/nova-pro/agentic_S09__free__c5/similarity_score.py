import numpy as np
from cohere import Client

co = Client(os.getenv('COHERE_API_KEY'))

def similarity_score(text1, text2):
    embeddings = co.embed(texts=[text1, text2])
    return np.dot(embeddings.embeddings[0], embeddings.embeddings[1])
