# Embed caption chunks into dense vectors for similarity search.
import asyncio
from sentence_transformers import SentenceTransformer
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from speech_client import get_speech_client

MODEL = "all-MiniLM-L6-v2"
embedder = SentenceTransformer(MODEL)

async def embed_captions(caption_queue: asyncio.Queue):
    """Yields vector embeddings for each caption chunk read from caption_queue."""
    client = get_speech_client()
    cfg = types.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )
    stream_cfg = types.StreamingRecognitionConfig(
        config=cfg,
        interim_results=True,
    )
    
    # Dummy audio generation for demo
    async def audio_gen():
        for i in range(3):
            yield b"dummy audio chunk"
            await asyncio.sleep(0.5)
    
    requests = (types.StreamingRecognizeRequest(audio_content=chunk) for chunk in audio_gen())
    async for resp in client.streaming_recognize(stream_cfg, requests):
        for result in resp.results:
            if result.is_final:
                txt = result.alternatives[0].transcript
                vec = embedder.encode(txt, convert_to_tensor=True).tolist()
                caption_queue.put_nowait(vec)

if __name__ == "__main__":
    q = asyncio.Queue()
    asyncio.run(embed_captions(q))

__all__ = []
