import cohere

COHERE_API_KEY = "your_api_key"


def platform_output_embedding(text):
    client = cohere.Client(COHERE_API_KEY)
    response = client.embed(texts=[text])
    return response.embeddings[0]
