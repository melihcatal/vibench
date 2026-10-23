from dashscope import Embeddings


def secret_audit_embedding(text, api_key):
    embeddings = Embeddings(api_key=api_key)
    response = embeddings.embed(text)
    return response
