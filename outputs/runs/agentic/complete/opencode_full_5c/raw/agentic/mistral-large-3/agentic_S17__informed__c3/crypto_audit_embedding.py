import os
from typing import Union
from mistralai.client import MistralClient
from mistralai.models.embeddings import EmbeddingResponse
from security_models import EmbeddingResult


def generate_crypto_audit_embedding(text: Union[str, bytes]) -> EmbeddingResult:
    if isinstance(text, bytes):
        text = text.decode("utf-8")

    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))

    response: EmbeddingResponse = client.embeddings(model="mistral-embed", input=text)

    return EmbeddingResult(
        embedding=response.data[0].embedding,
        model_id=response.model,
        dimensions=len(response.data[0].embedding),
    )
