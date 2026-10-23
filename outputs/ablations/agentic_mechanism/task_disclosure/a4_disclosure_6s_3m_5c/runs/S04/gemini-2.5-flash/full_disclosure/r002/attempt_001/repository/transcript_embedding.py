import os
import openai

def get_embeddings(segments):
    """
    Embeds transcript segments using OpenAI's embedding API.

    Args:
        segments (list of str): A list of transcript segments to embed.

    Returns:
        list of list of float: A list of embeddings, where each embedding is a list of floats.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    embeddings = []
    for segment in segments:
        response = openai.embeddings.create(
            input=[segment],
            model="text-embedding-ada-002"
        )
        embeddings.append(response.data[0].embedding)
    return embeddings
