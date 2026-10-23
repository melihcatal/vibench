from google import genai

from storage_models import EmbeddingResult


def asset_metadata_embedding(metadata_text: str, extracted_text: str, model: str = "text-embedding-004") -> EmbeddingResult:
    client = genai.Client()
    response = client.models.embed_content(model=model, contents=[f"{metadata_text}\n{extracted_text}"])
    vector = list(response.embeddings[0].values) if response.embeddings else []
    return EmbeddingResult(vector=vector, dimensions=len(vector), provider="google")
