from embeddings_client import get_gemini_client
from embeddings_models import normalize_text_input, parse_embedding_response

def embed_batch(texts: list[str]) -> list[list[float]]:
    genai = get_gemini_client()
    normalized_texts = [normalize_text_input(text) for text in texts]
    response = genai.embed_content(model="models/embedding-001", content=normalized_texts)
    return [parse_embedding_response(item) for item in response['embeddings']]
