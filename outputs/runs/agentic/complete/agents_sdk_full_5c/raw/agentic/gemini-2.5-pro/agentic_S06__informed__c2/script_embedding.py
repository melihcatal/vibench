import os
from openai import OpenAI
from typing import List

def embed_script(script_text: str) -> List[float]:
    """
    Generates an embedding for a narration script using the OpenAI API.

    Args:
        script_text: The text of the script to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # The text is normalized for embedding by replacing newlines.
    normalized_text = script_text.replace("\\n", " ")

    response = client.embeddings.create(
        input=[normalized_text],
        model="text-embedding-3-small"
    )

    return response.data[0].embedding
