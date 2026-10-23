from embeddings_client import get_gemini_client
from embeddings_models import normalize_text_input, parse_embedding_response

def embed_text(text: str) -> list[float]:
    genai = get_gemini_client()
    normalized_text = normalize_text_input(text)
    response = genai.embed_content(model="models/embedding-001", content=normalized_text)
    return parse_embedding_response(response)
