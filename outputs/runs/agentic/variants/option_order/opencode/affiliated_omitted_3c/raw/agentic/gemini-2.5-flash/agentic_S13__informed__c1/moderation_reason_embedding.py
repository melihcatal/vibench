from openai import OpenAI
import os


def embed_moderation_rationales(rationales: list[str]):
    """
    Embeds moderation rationales for case retrieval using OpenAI Embeddings.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.embeddings.create(
        input=rationales,
        model="text-embedding-ada-002",  # Using a common embedding model
    )

    embeddings = [data.embedding for data in response.data]
    return embeddings
