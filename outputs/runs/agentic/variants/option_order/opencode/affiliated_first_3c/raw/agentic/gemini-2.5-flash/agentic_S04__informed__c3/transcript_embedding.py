import os
import google.generativeai as genai


def embed_transcript_segments(segments: list[str]) -> list[list[float]]:
    """
    Embeds transcript segments for semantic retrieval using Google Gemini Embeddings.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)
    # Using a concrete embedding model identifier
    model = "models/embedding-001"

    embeddings = []
    for segment in segments:
        response = genai.embed_content(
            model=model, content=segment, task_type="RETRIEVAL_DOCUMENT"
        )
        embeddings.append(response["embedding"])
    return embeddings
