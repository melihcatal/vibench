from openai import OpenAI


def secret_audit_embedding(api_key, text):
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(input=text, model="text-embedding-ada-002")
    return response.data[0].embedding
