import os
import google.generativeai as genai


def embed_transcript_segment(segment_text: str) -> list[float]:
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)

    # Use the embedding-001 model for embeddings
    model = "models/embedding-001"

    response = genai.embed_content(model=model, content=segment_text)
    return response["embedding"]
