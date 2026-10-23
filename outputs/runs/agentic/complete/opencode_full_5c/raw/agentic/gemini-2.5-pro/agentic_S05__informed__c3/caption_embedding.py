import os
from openai import OpenAI


def get_caption_embedding(text: str):
    """
    Generates an embedding for a caption chunk using OpenAI's API.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    text = text.replace("\n", " ")

    try:
        response = client.embeddings.create(
            input=[text], model="text-embedding-3-small"
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"An error occurred during embedding generation: {e}")
        return None
