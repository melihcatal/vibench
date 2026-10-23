import openai


def secret_audit_embedding(api_key, text):
    openai.api_key = api_key
    response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
    return response["data"][0]["embedding"]
