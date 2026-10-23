import os
import requests
from speech_models import TranscriptionUtterance


def embed_transcript_segments(
    segments: list[TranscriptionUtterance],
) -> list[list[float]]:
    """
    Embeds transcript segments for semantic retrieval using a Hugging Face model.
    """
    hf_token = os.environ.get("HUGGINGFACE_HUB_TOKEN")
    api_url = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
    headers = {"Authorization": f"Bearer {hf_token}"}

    texts = [segment.text for segment in segments]

    if not texts:
        return []

    response = requests.post(api_url, headers=headers, json={"inputs": texts})
    response.raise_for_status()

    return response.json()
