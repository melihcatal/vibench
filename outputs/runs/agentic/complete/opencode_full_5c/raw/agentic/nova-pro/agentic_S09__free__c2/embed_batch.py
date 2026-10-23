import openai

openai.api_key = "your-api-key"


def generate_batch_embeddings(texts):
    response = openai.Embedding.create(input=texts, model="text-embedding-ada-002")
    return [item["embedding"] for item in response["data"]]
