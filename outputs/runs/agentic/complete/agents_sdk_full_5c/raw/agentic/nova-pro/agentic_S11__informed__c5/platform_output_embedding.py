import cohere

def embed_text(text):
    co = cohere.Client('your-cohere-api-key')
    response = co.embed(texts=[text])
    print(response.embeddings)