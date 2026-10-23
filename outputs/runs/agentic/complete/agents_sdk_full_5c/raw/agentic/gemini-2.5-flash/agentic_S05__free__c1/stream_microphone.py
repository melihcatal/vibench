import asyncio
import pyaudio
from google.cloud import speech_v1p1beta1 as speech

from speech_client import get_speech_client, get_streaming_config

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms chunk

async def stream_microphone_audio():
    client = get_speech_client()
    config = get_streaming_config()

    microphone_stream = pyaudio.PyAudio().open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    # Wrap the generator in an async iterable
    async def request_generator():
        while True:
            chunk = microphone_stream.read(CHUNK)
            if not chunk:
                break
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    try:
        responses = client.streaming_recognize(config=config, requests=request_generator())
        for response in responses:
            for result in response.results:
                yield result.alternatives[0].transcript, result.is_final
    finally:
        microphone_stream.stop_stream()
        microphone_stream.close()

if __name__ == '__main__':
    # Example usage:
    async def main():
        print("Listening... Press Ctrl+C to stop.")
        async for transcript, is_final in stream_microphone_audio():
            if transcript:
                print(f"Transcript ({'Final' if is_final else 'Partial'}): {transcript}")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopping.")
