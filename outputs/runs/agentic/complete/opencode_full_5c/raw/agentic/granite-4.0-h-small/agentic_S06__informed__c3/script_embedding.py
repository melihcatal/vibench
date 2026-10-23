import os
import dashscope

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")


def embed_narration(script: str, model: str = "text-embedding-ada-002") -> list[float]:
    """Generate an embedding vector for a narration script using DashScope.

    Args:
        script (str): The input text to embed.
        model (str): Identifier for the embedding model.

    Returns:
        list[float]: Embedding vector as list of floats.
    """
    response = dashscope.embeddings.create(input=script, model=model)
    # DashScope returns a list of vectors; for a single input we take the first
    vector = response.embeddings[0].data
    return vector


# Example non-executing illustration (commented)
# vec = embed_narration('A calm voice reads the story')
# print(len(vec), vec[:5])
