from numpy import dot
from numpy.linalg import norm
from.embeddings_client import get_text_analytics_client

def similarity_score(text1, text2):
    client = get_text_analytics_client()
    embedding1 = client.single_embed(text1).embedding
    embedding2 = client.single_embed(text2).embedding
    return dot(embedding1, embedding2)/(norm(embedding1)*norm(embedding2))

if __name__ == '__main__':
    print(similarity_score('Hello, world!', 'Goodbye, world!'))