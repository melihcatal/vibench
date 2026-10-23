import os
import google.generativeai as genai


def embed_transcript_segment(segment: str) -> list[float]:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = "models/embedding-001"
    response = genai.embed_content(model=model, content=segment)
    return response["embedding"]
