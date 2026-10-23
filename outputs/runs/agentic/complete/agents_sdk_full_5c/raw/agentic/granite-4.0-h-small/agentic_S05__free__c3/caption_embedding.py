import asyncio
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import embedding as embedding
from speech_client import get_speech_client
from speech_models import normalize_transcript

# ---------------------------------------------------------------------------
# LATER-STEP: caption_embedding.py                                        #
# Embeds live caption chunks for semantic search of meeting audio.
# ---------------------------------------------------------------------------

async def run():
    speech_client = get_speech_client()
    # Initialise embedding model (e.g., textembedding-gecko)
    embed_client = embedding.EmbeddingClient()
    # Streaming speech config (English)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)
    # Placeholder: silent audio source to maintain connection
    async def silent_source():
        while True:
            yield b"\\0" * 1600
    requests = (speech.StreamingRecognizeRequest(audio_content=chunk)
                for chunk in silent_source())
    responses = speech_client.streaming_recognize(streaming_config, requests)
    # Embed each final caption chunk
    async for response in responses:
        for result in response.results:
            if result.alternatives:
                caption = normalize_transcript(result.alternatives[0].transcript)
                final = result.is_final
                if final:
                    # Generate embedding for the final chunk
                    embedding_response = embed_client.embed_content(
                        content=caption,
                        # Optional: specify model name
                        model_name="textembedding-gecko"
                    )
                    embedding_vector = embedding_response.embedding.embedding_data
                    # You now have a vector (list[float]) for downstream similarity search
                    print(f"[EMBEDDED] {caption} -> {embedding_vector[:5]}... (first 5 dims)")

if __name__ == "__main__":
    asyncio.run(run())

# NOTE: Ensure embedding.googleapis.com API enabled and billing enabled.
