import os
from cohere import Client

client = Client(os.getenv('COHERE_API_KEY'))

def similarity_score(text1, text2):
    embeddings = client.embed(texts=[text1, text2]).embeddings
    similarity = sum(e1 * e2 for e1, e2 in zip(embeddings[0], embeddings[1])) / (sum(e1**2 for e1 in embeddings[0]) * sum(e2**2 for e2 in embeddings[1]))**0.5
    return similarity

if __name__ == '__main__':
    print(similarity_score('sample text 1', 'sample text 2'))