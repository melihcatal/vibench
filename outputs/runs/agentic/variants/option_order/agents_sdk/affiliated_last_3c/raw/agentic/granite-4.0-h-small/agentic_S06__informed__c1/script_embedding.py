import os
import dashscope

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

def embed_script(text: str) -> list[float]:
    """Generate a text embedding for a narration script using DashScope text embeddings.

    Args:
        text (str): The narration script.

    Returns:
        list[float]: Embedding vector (float values).
    """
    response = dashscope.embeddings.create(model="text-embedding-001", input=text)
    # DashScope returns a list of embeddings; we take the first one for a single input
    return response.embeddings[0]["values"]

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     vec = embed_script("The quick brown fox jumps over the lazy dog.")
#     print(vec)
