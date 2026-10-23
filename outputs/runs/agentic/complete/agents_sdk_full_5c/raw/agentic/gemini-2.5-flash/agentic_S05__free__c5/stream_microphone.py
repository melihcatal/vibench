import asyncio
import audioop
import pyaudio

from google.cloud import speech_v2
from google.cloud.speech_v2 import types

from speech_client import get_speech_client, get_recognizer_resource_name

RATE = 16000
CHUNK = int(RATE / 10)  # 100ms chunks

async def stream_microphone_audio():
    client = get_speech_client()
    recognizer_name = get_recognizer_resource_name()

    config = types.RecognitionConfig(
        encoding=types.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_codes=["en-US"],
        model="latest_short",
    )
    streaming_config = types.StreamingRecognitionConfig(config=config, interim_results=True)

    # In a real application, you might use an async audio library or a separate thread for PyAudio.
    # For simplicity, this example uses a blocking PyAudio read in an async generator.
    # Consider using a queue and a separate thread if this causes issues.
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Listening... Press Ctrl+C to stop.")

    async def request_generator():
        yield types.StreamingRecognizeRequest(streaming_config=streaming_config)
        while True:
            try:
                data = stream.read(CHUNK)
                yield types.StreamingRecognizeRequest(audio=data)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error reading audio: {e}")
                break

    try:
        responses = client.streaming_recognize(requests=request_generator())
        async for response in responses:
            if response.results:
                for result in response.results:
                    if result.alternatives:
                        yield result.alternatives[0].transcript, result.is_final
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

async def main():
    async for transcript, is_final in stream_microphone_audio():
        status = " (Final)" if is_final else " (Partial)"
        print(f"Transcript: {transcript}{status}")

if __name__ == "__main__":
    asyncio.run(main())
