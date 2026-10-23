import dashscope


def embed_batch(texts):
    dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
    response = dashscope.TextEmbedding.create(model="text-embedding-v1", input=texts)
    return [item.embedding for item in response.data]
