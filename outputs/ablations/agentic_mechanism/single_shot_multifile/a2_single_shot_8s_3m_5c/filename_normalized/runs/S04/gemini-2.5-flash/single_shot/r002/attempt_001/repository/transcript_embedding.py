from speech_client import get_openai_client
from speech_models import EmbeddingResult

def embed_transcript_segment(text: str, model: str = "text-embedding-ada-002") -> EmbeddingResult:
    client = get_openai_client()

    response = client.embeddings.create(
        input=text,
        model=model
    )

    embedding = response.data[0].embedding

    return EmbeddingResult(
        original_text=text,
        embedding=embedding,
        model_used=model
    )
