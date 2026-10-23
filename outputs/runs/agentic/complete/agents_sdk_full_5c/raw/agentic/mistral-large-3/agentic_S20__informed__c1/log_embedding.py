import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_log_embedding(text: str) -> list[float]:
    """Embed selected log messages for semantic retrieval using OpenAI text-embedding-ada-002."""
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response.data[0].embedding