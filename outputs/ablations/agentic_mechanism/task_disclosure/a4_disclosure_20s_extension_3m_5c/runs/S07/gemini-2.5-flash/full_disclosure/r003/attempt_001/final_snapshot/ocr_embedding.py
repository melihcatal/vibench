import openai
import os

def embed_document_section(text: str) -> list[float]:
    """
    Embeds a document section using OpenAI's text-embedding-ada-002 model.

    Args:
        text: The text content of the document section to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    response = openai.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding
