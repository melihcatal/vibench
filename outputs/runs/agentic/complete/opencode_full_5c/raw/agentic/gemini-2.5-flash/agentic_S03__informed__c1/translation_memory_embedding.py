from translation_client import get_gemini_client
import google.generativeai as genai
import os


def embed_translated_segment(segment: str) -> list[float]:
    genai = get_gemini_client()
    model = "models/embedding-001"  # Using specific embedding model ID

    # The Gemini API's embedding model expects a list of strings
    response = genai.embed_content(model=model, content=[segment])

    # The embedding is a list of floats for the single segment
    return response["embedding"]
