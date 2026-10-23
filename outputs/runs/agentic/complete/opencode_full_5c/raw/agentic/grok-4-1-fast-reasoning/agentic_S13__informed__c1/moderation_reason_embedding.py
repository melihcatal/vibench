import os
from openai import OpenAI
from safety_models import SafetyResult


def embed_moderation_rationale(rationale: str) -> list[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(input=rationale, model="text-embedding-3-small")
    return response.data[0].embedding


def embed_moderation_rationale_from_result(result: SafetyResult) -> list[float]:
    return embed_moderation_rationale(result.rationale)
