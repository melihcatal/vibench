import openai
import os

def embed_sections(sections: list[str]) -> list[list[float]]:
    """
    Embeds a list of text sections using OpenAI's text-embedding-ada-002 model.

    Args:
        sections: A list of text strings, where each string is a document section.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    client = openai.OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    response = client.embeddings.create(
        input=sections,
        model="text-embedding-ada-002"
    )
    return [data.embedding for data in response.data]
