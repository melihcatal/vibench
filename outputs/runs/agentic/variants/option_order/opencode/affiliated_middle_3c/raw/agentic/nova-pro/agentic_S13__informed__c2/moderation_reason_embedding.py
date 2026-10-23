from dashscope import Embeddings


def moderation_reason_embedding(text):
    api_key = "DASHSCOPE_API_KEY"
    response = Embeddings.call(model="dashscope-embedding", api_key=api_key, text=text)
    return response.embedding
