import asyncio

# Google Cloud Speech-to-Text
from google.cloud import speech_v1p1beta1 as speech

# Helper utilities from local modules
from speech_client import get_speech_client

# Configuration (could be loaded from env vars)
LANGUAGE_CODE = "es-ES"          # Spanish (Spain) as example
SAMPLE_RATE_HZ = 16000
CHUNK_SIZE = 1024
INTERIM_RESULTS = True

async def stream_with_language():
    """Start a streaming recognizer that uses a specific language and punctuation settings."""
    client = get_speech_client()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=SAMPLE_RATE_HZ,
        language_code=LANGUAGE_CODE,
        enable_automatic_punctuation=INTERIM_RESULTS,
        speech_contexts=[
            # Example: boost words that are common in this domain
            speech.SpeechContext(phrases=["conferencia", "reunión"], boost=5.0)
        ],
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=INTERIM_RESULTS,
    )
    # Audio generator placeholder (use the same as in stream_microphone)
    async def audio_generator():
        import pyaudio
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                         channels=1,
                         rate=SAMPLE_RATE_HZ,
                         input=True,
                         frames_per_buffer=CHUNK_SIZE)
        try:
            while True:
                data = stream.read(CHUNK_SIZE)
                yield data
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
    audio_gen = audio_generator()
    requests = [speech.StreamingRecognizeRequest(audio_content=chunk)
                for chunk in audio_gen]
    async with client.streaming_recognize(streaming_config, requests) as response_stream:
        async for result in response_stream:
            if result.results:
                for r in result.results:
                    if r.alternatives:
                        print(f"{'INTERIM' if not r.is_final else 'FINAL'}: {r.alternatives[0].transcript}")

if __name__ == "__main__":
    asyncio.run(stream_with_language())
