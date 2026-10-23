from observability_client import get_gemini_client


def get_log_embedding(text: str) -> list[float]:
    genai = get_gemini_client()
    response = genai.embed_content(model="models/embedding-001", content=text)
    return response["embedding"]
