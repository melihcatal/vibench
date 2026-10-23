import os
import dashscope

# DashScope API key
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

def embed_text(text: str, model: str = "text-embedding-ada-002") -> list[float]:
    """Embeds arbitrary text using DashScope's embedding endpoint.

    Returns a list of float values representing the embedding vector.
    """
    response = dashscope.embeddings.create(
        model=model,
        inputs=[text],
        temperature=0.0,
    )
    # response.raw.embeddings is a list of Embedding objects
    vec = response.raw.embeddings[0].embedding  # list[float]
    return vec

# Example usage
# if __name__ == "__main__":
#     vec = embed_text("The quick brown fox jumps over the lazy dog")
#     print(vec)
