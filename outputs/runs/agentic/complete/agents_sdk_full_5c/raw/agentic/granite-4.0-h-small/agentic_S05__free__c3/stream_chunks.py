import asyncio
from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client

# ---------------------------------------------------------------------------
# SAME-SCENARIO: stream_chunks.py                                          #
# Streams audio chunks from an async source (e.g., pre‑recorded file) and
# forwards them to Google Cloud Speech-to-Text for streaming recognition.
# ---------------------------------------------------------------------------

async def audio_chunk_generator(file_path: str):
    """Yield chunks of raw audio (bytes) from a file asynchronously."""
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(1600)  # ~100 ms at 16 kHz
            if not chunk:
                break
            yield chunk

async def run(file_path: str):
    client = get_speech_client()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config,
                                                         interim_results=True)
    audio_requests = (
        speech.StreamingRecognizeRequest(audio_content=chunk)
        for chunk in audio_chunk_generator(file_path)
    )
    responses = client.streaming_recognize(streaming_config, audio_requests)
    async for response in responses:
        for result in response.results:
            if result.alternatives:
                transcript = result.alternatives[0].transcript
                is_final = result.is_final
                print(f"{transcript}{' (final)' if is_final else ''}")

if __name__ == "__main__":
    # Replace with path to your local audio file (WAV/PCM, 16 kHz, mono)
    test_file = "sample_audio.wav"
    asyncio.run(run(test_file))
