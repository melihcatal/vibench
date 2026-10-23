import pyaudio
import asyncio
from speech_client import get_speech_client
from partial_results import handle_partial_results

p = pyaudio.PyAudio()

async def stream_microphone():
    client = get_speech_client()
    stream = await client.streaming_recognize(
        config={
            "model": "whisper-1",
            "language": "en",
            "response_format": "text",
            "punctuation": True,
        },
        audio_input_queue=asyncio.Queue(),
    )

    def microphone_callback(in_data, frame_count, time_info, status):
        asyncio.run_coroutine_threadsafe(stream.send_audio(in_data), loop=asyncio.get_event_loop())
        return (in_data, pyaudio.paContinue)

    audio_stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1024,
        stream_callback=microphone_callback,
    )

    audio_stream.start_stream()
    try:
        async for transcript in handle_partial_results(stream):
            yield transcript
    finally:
        audio_stream.stop_stream()
        audio_stream.close()