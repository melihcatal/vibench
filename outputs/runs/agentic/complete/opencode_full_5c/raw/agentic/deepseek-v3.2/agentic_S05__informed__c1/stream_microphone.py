import asyncio
import pyaudio
from deepgram import Deepgram
import os


async def stream_microphone():
    dg_client = Deepgram(os.getenv("DEEPGRAM_API_KEY"))

    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024

    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )

    try:
        async with dg_client.transcription.live(
            {
                "model": "nova-2",
                "interim_results": True,
                "smart_format": True,
                "encoding": "linear16",
                "sample_rate": RATE,
                "channels": CHANNELS,
            }
        ) as connection:

            async def send_audio():
                while True:
                    data = stream.read(CHUNK, exception_on_overflow=False)
                    await connection.send(data)
                    await asyncio.sleep(0)

            async def receive_results():
                async for message in connection:
                    if "channel" in message:
                        for alternative in message["channel"]["alternatives"]:
                            if "transcript" in alternative:
                                transcript = alternative["transcript"]
                                if transcript:
                                    yield transcript, message.get("is_final", False)

            send_task = asyncio.create_task(send_audio())

            try:
                async for transcript, is_final in receive_results():
                    yield transcript, is_final
            finally:
                send_task.cancel()
                try:
                    await send_task
                except asyncio.CancelledError:
                    pass

    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()


async def main():
    async for transcript, is_final in stream_microphone():
        prefix = "[INTERIM]" if not is_final else "[FINAL]"
        print(f"{prefix} {transcript}")


if __name__ == "__main__":
    asyncio.run(main())
