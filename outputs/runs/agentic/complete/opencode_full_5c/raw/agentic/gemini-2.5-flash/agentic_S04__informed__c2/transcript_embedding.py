import google.generativeai as genai
import os


def get_transcript_embedding(segment_text: str) -> list[float]:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("embedding-001")
    response = model.embed_content(
        content=segment_text, task_type="SEMANTIC_SIMILARITY"
    )
    return response.embedding
