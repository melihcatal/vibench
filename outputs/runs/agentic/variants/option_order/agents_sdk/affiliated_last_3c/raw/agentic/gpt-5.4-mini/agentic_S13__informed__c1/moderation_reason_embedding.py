from __future__ import annotations

from openai import OpenAI

from safety_models import EmbeddingJob


client = OpenAI()


def moderation_reason_embedding(job: EmbeddingJob):
    response = client.embeddings.create(model="text-embedding-3-small", input=job.text)
    return response.data[0].embedding
