from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed_moderation_rationale(rationale: str) -> list[float]:
    response = client.embeddings.create(
        input=rationale,
        model="text-embedding-3-small"
    )
    return [float(x) for x in response.data[0].embedding]