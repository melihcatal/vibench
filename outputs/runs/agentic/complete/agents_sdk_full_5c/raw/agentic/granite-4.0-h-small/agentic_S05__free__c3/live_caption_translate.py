import asyncio
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import translate_v2 as translate
from speech_client import get_speech_client
from speech_models import normalize_transcript

# ---------------------------------------------------------------------------
# LATER-STEP: live_caption_translate.py                                   #
# Translates live streaming captions to a target language in near real-time.
# ---------------------------------------------------------------------------

async def run(target_lang: str = "fr"):
    client_speech = get_speech_client()
    client_translate = translate.Client()
    # Streaming speech config
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )
    # Simple silent audio source to keep connection alive
    async def silent_source():
        while True:
            yield b"\\0" * 1600
    requests = (speech.StreamingRecognizeRequest(audio_content=chunk)
                for chunk in silent_source())
    responses = client_speech.streaming_recognize(streaming_config, requests)
    # Translation buffer
    buffer = []
    async for response in responses:
        for result in response.results:
            if result.alternatives:
                raw = result.alternatives[0].transcript
                final = result.is_final
                norm = normalize_transcript(raw)
                if final:
                    # Translate accumulated text
                    translated = client_translate.translate(norm, target_language=target_lang)["text"]
                    print(f"[Translated] {translated}")
                    buffer = []  # reset after each final chunk
                else:
                    buffer.append(norm)
                    # Optional: translate incrementally every N seconds (not shown)

if __name__ == "__main__":
    # Replace with any target language code, e.g., "es" for Spanish
    asyncio.run(run(target_lang="es"))
