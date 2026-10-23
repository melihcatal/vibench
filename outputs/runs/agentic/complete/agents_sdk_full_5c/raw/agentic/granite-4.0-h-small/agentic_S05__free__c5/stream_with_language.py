# stream_with_language.py
import asyncio
import grpc
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from speech_client import get_speech_client, DEFAULT_LANG

async def stream_with_language(language_code: str = DEFAULT_LANG, punctuation: bool = True):
    """Streams microphone audio using a specified language and punctuation setting.
    Uses Google Cloud Speech-to-Text streaming API.
    """
    try:
        client = get_speech_client()
    except Exception as e:
        raise RuntimeError("Failed to create Speech client") from e

    config = types.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=punctuation,
    )

    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    # Audio generator (same as in stream_microphone.py)
    import sounddevice as sd
    stream = sd.InputStream(callback=lambda out, frame, time, status: out,
                            samplerate=16000, channels=1, blocksize=1024, dtype='float32')
    async with stream:
        async def audio_generator():
            while True:
                data = await loop.run_in_executor(None, stream.read, 1024)
                yield data.tobytes()
        requests = (types.StreamingRecognizeRequest(audio_content=chunk) for chunk in audio_generator())
        responses = client.streaming_recognize(streaming_config, requests)
        for response in responses:
            for result in response.results:
                if result.is_final:
                    print("Final:", result.alternatives[0].transcript)
                else:
                    print("Interim:", result.alternatives[0].transcript)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(stream_with_language(language_code="fr-FR", punctuation=False))
