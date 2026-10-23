import asyncio
import pyaudio
from google.cloud import speech_v1p1beta1 as speech

from speech_client import get_speech_client

# Audio recording parameters (same as stream_microphone for consistency)
RATE = 16000
CHUNK = int(RATE / 10)

async def stream_with_language_and_punctuation(language_code: str = 'en-US', enable_automatic_punctuation: bool = True):
    client = get_speech_client()

    audio_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=audio_config,
        interim_results=True,
    )

    microphone_stream = pyaudio.PyAudio().open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    async def request_generator():
        while True:
            chunk = microphone_stream.read(CHUNK)
            if not chunk:
                break
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    try:
        print(f"Listening with language '{language_code}' and punctuation {'enabled' if enable_automatic_punctuation else 'disabled'}...")
        responses = client.streaming_recognize(config=streaming_config, requests=request_generator())
        for response in responses:
            for result in response.results:
                yield result.alternatives[0].transcript, result.is_final
    finally:
        microphone_stream.stop_stream()
        microphone_stream.close()

if __name__ == '__main__':
    async def main():
        print("Starting speech recognition with specific language and punctuation.")
        # Example: Recognize in French with punctuation
        async for transcript, is_final in stream_with_language_and_punctuation(language_code='fr-FR', enable_automatic_punctuation=True):
            if transcript:
                print(f"Transcript ({'Final' if is_final else 'Partial'}): {transcript}")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopping.")
