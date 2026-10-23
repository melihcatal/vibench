import os
from typing import List
from speech_models import TranscriptionResult
from google.cloud import genai


def transcript_embedding(transcript: str, model: str = "gemini-1.5-pro") -> List[str]:
    """Embed each sentence of a transcript using Google Gemini embeddings.

    Returns a list of embedding vectors (as strings) for downstream retrieval.
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    embedder = genai.Embedding(model)
    sentences = [s.strip() for s in transcript.split(".") if s.strip()]
    embeddings = []
    for sent in sentences:
        response = embedder.embed_content(sent)
        # response.embeddings is a list of Embedding objects; we keep the vector as a list of floats
        embeddings.append(str([float(v) for v in response.embeddings[0].embedding]))
    return embeddings


# Example
# vecs = transcript_embedding(raw_transcript)
