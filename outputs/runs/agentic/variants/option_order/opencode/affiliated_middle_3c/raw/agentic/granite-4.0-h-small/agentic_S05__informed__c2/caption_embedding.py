import json
import numpy as np
from speech_models import normalize_transcript, SpeechRecognitionResult

# OpenAI embeddings API (example)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_ENDPOINT = "https://api.openai.com/v1/embeddings"


def embed_caption(text: str) -> np.ndarray:
    """Generates an embedding for a caption chunk using OpenAI's embeddings API.
    Args:
        text (str): caption fragment
    Returns:
        np.ndarray: embedding vector (typically 1536-d)
    """
    payload = {"model": "text-embedding-ada-002", "input": text}
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    resp = requests.post(EMBEDDING_ENDPOINT, json=payload, headers=headers)
    data = resp.json()
    # Embedding vectors are under data['data'][0]['embedding']
    vec = np.array(data["data"][0]["embedding"])
    return vec


# Sample usage with streaming chunks (placeholder)
# embeddings = []
# async for chunk in stream_microphone():
#     result = json.loads(chunk)
#     if result.get('is_final'):
#         caption = normalize_transcript(result)
#         vec = embed_caption(caption)
#         embeddings.append(vec)
#         # Store or index vec for semantic search later
