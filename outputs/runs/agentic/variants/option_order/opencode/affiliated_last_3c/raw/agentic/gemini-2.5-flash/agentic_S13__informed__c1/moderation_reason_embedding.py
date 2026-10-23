from safety_client import GeminiClient
from safety_models import EmbeddingResult


def embed_moderation_rationale(rationale_text: str) -> EmbeddingResult:
    client = GeminiClient()
    embedding = client.embed_content(rationale_text)
    return EmbeddingResult(text=rationale_text, embedding=embedding)
