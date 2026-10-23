# [LATER-STEP] caption_embedding.py
import asyncio

import speech_client as sc
from speech_models import StreamingRecognitionResult, normalize_provider_result

# Provider: Cohere Embed API (provider identified via COHERE_API_KEY usage in embedded client code)

async def embed_captions(source_iterable, model_id="embed-english-v3.0"):
    """
    Stream live audio, transcribe captions, and embed each finalized caption chunk
    for semantic search or retrieval.
    
    Args:
        source_iterable: async generator yielding raw PCM audio bytes.
        model_id: Cohere embedding model identifier (provider-specific).
    """
    async for result in sc.recognize_streaming(source_iterable):
        if not result.is_partial:
            cap = normalize_provider_result(result)
            caption = cap.alternatives[0].transcript
            embedding = await embed_text(caption, model_id=model_id)
            # Return a dict suitable for downstream indexing / similarity search
            yield {"transcript": caption, "embedding": embedding.tolist()}

async def embed_text(text: str, model_id: str = "embed-english-v3.0") -> "numpy.ndarray":
    """
    Call Cohere Embed API (provider SDK) and return a 1-D vector (list of floats).
    """
    from cohere import Cohere
    # Provider identification via the client creation (COHERE_API_KEY env var)
    co = Cohere(api_key="")  # placeholder; key is expected in env
    response = co.embeddings(model=model_id, texts=[text])
    # Cohere returns a list of Embedding objects with .embedding attribute
    vec = response.embeddings[0].embedding
    return vec

# Example driver (mute):
# async def mic():
#     for chunk in sc.microphone_generator():
#         yield chunk
# async for emb in embed_captions(mic()):
#     print(emb)
