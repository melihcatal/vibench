import openai


def crypto_audit_embedding(text):
    openai.api_key = "your_openai_api_key"
    response = openai.Embedding.create(input=text)
    return response["data"][0]["embedding"]
