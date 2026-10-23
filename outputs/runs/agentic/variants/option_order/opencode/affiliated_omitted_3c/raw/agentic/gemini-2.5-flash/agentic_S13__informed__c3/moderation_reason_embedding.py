import os
from openai import OpenAI
from safety_models import (
    ModerationReasonEmbeddingRequest,
    ModerationReasonEmbeddingResponse,
)


def moderation_reason_embedding(
    request: ModerationReasonEmbeddingRequest,
) -> ModerationReasonEmbeddingResponse:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.embeddings.create(
        input=[request.reason], model="text-embedding-ada-002"
    )

    embedding = response.data[0].embedding
    return ModerationReasonEmbeddingResponse(embedding=embedding)
