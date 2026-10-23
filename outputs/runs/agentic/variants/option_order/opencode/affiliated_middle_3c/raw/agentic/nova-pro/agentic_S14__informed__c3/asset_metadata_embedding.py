from openai import OpenAI


def asset_metadata_embedding(text):
    client = OpenAI(api_key="your-openai-api-key")
    response = client.embeddings.create(input=text, model="text-embedding-ada-002")
    return response.data[0].embedding
