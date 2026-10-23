import cohere

co = cohere.Client('YOUR_COHERE_API_KEY')

def get_embedding(text):
    response = co.embed(texts=[text])
    return response.embeddings[0]