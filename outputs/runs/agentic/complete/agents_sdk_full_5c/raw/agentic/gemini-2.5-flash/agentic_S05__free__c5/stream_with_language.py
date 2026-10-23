import asyncio
import collections
import pyaudio

from google.cloud import speech_v2
from google.cloud.speech_v2 import types

from speech_client import get_speech_client, get_recognizer_resource_name
from partial_results import handle_streaming_results

RATE = 16000
CHUNK = int(RATE / 10)  # 100ms chunks

async def stream_recognize_with_settings(
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
    audio_source_generator=None
):
    client = get_speech_client()
    recognizer_name = get_recognizer_resource_name()

    config = types.RecognitionConfig(
        encoding=types.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_codes=[language_code],
        model="latest_long", # Use 'latest_long' for better accuracy over time
        enable_automatic_punctuation=enable_automatic_punctuation,
    )
    streaming_config = types.StreamingRecognitionConfig(config=config, interim_results=True)

    audio_queue = asyncio.Queue()

    # Setup PyAudio for microphone input if no custom generator is provided
    p_audio_stream = None
    p_audio_instance = None

    if audio_source_generator is None:
        p_audio_instance = pyaudio.PyAudio()
        p_audio_stream = p_audio_instance.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
            stream_callback=lambda in_data, frame_count, time_info, status: (
                asyncio.run_coroutine_threadsafe(audio_queue.put(in_data), asyncio.get_event_loop()),
                pyaudio.paContinue
            )
        )
        p_audio_stream.start_stream()
        print(f"Listening with language '{language_code}', punctuation: {enable_automatic_punctuation}...")

    async def request_generator():
        yield types.StreamingRecognizeRequest(streaming_config=streaming_config)
        while True:
            try:
                if audio_source_generator:
                    chunk = await anext(audio_source_generator)
                else:
                    chunk = await audio_queue.get()
                yield types.StreamingRecognizeRequest(audio=chunk)
            except (StopAsyncIteration, asyncio.CancelledError, KeyboardInterrupt):
                break
            except Exception as e:
                print(f"Error in request generator: {e}")
                break

    try:
        responses = client.streaming_recognize(requests=request_generator())
        async for transcript, is_final in handle_streaming_results(responses):
            yield transcript, is_final
    finally:
        if p_audio_stream:
            p_audio_stream.stop_stream()
            p_audio_stream.close()
            p_audio_instance.terminate()

async def main():
    print("\n--- English (en-US) with punctuation ---")
    async for transcript, is_final in stream_recognize_with_settings(language_code="en-US", enable_automatic_punctuation=True):
        pass # handle_streaming_results already prints

    # You could add another language here, e.g., 'es-ES' if you have an input for it.
    # print("\n--- Spanish (es-ES) without punctuation (requires Spanish audio input) ---")
    # async for transcript, is_final in stream_recognize_with_settings(language_code="es-ES", enable_automatic_punctuation=False):
    #     pass

if __name__ == "__main__":
    asyncio.run(main())
