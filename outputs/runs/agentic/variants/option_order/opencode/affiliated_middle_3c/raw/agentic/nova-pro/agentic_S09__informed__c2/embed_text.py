import dashscope


def embed_text(text):
    dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
    response = dashscope.TextEmbedding.create(model="text-embedding-v1", input=text)
    return response.data[0].embedding
