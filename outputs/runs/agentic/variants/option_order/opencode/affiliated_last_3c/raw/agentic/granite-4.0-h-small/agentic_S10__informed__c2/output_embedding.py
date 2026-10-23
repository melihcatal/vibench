import dashscope

# Provider: DashScope Embeddings API

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")


def embed_text(text: str) -> list[float]:
    """Return a dense embedding vector (list of floats) for the input text."""
    if not DASHSCOPE_API_KEY:
        raise ValueError("Set DASHSCOPE_API_KEY environment variable")
    client = dashscope.Embeddings(api_key=DASHSCOPE_API_KEY)
    resp = client.embeddings(model="qwen", inputs=[text])
    # Embeddings API returns a list of vectors; we take the first (and only) one
    return resp.embeddings[0]
