import asyncio
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import content_safety_v1beta as content_safety
from speech_client import get_speech_client
from speech_models import normalize_transcript

# ---------------------------------------------------------------------------
# LATER-STEP: live_caption_safety.py                                      #
# Checks live caption text for unsafe content using Google Cloud Content
# Safety API and prints warnings.
# ---------------------------------------------------------------------------

async def run():
    speech_client = get_speech_client()
    safety_client = content_safety.Client()
    # Streaming speech config (English)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)
    # Simple silent audio source placeholder
    async def silent_source():
        while True:
            yield b"\\0" * 1600
    requests = (speech.StreamingRecognizeRequest(audio_content=chunk)
                for chunk in silent_source())
    responses = speech_client.streaming_recognize(streaming_config, requests)
    # Process each final transcript for safety
    async for response in responses:
        for result in response.results:
            if result.alternatives:
                text = normalize_transcript(result.alternatives[0].transcript)
                final = result.is_final
                if final:
                    # Call Content Safety API
                    response = safety_client.analyze_content(text)
                    unsafe = response.safe
                    if not unsafe:
                        print(f"[SAFE] {text}")
                    else:
                        # Example: block or flag unsafe words
                        unsafe_words = response.unsafe_categories[0].unsafe_words
                        print(f"[WARNING] Unsafe content detected: {unsafe_words}")

if __name__ == "__main__":
    asyncio.run(run())
