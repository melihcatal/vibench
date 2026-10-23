import dashscope

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")


def embed_text(texts):
    """Generate embeddings for a list of texts using DashScope embeddings."""
    client = dashscope.Embeddings(
        api_key=DASHSCOPE_API_KEY, model="text-embedding-ada-002"
    )
    response = client.embeddings(input=texts)
    # response format follows OpenAI style
    return [item.embedding for item in response.data]
