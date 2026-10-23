import openai

openai.api_key = "your-api-key"


def generate_embedding(text):
    response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
    return response["data"][0]["embedding"]
