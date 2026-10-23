from speech_client import get_speech_client
from speech_models import EmbeddingRequest


def embed_script(request: EmbeddingRequest) -> list[float]:
    client = get_speech_client().generative_ai_client
    # The embedding model to use for Gemini is 'embedding-001' or similar
    # Using the most common one. Ensure GOOGLE_API_KEY is set.
    response = client.embed_content(model="models/embedding-001", content=request.text)
    return response["embedding"]
