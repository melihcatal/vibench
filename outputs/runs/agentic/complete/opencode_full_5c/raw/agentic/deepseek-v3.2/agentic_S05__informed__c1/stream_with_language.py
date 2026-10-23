import asyncio
from deepgram import Deepgram
import os


async def start_streaming_recognizer(
    language: str = "en", enable_punctuation: bool = True
):
    dg_client = Deepgram(os.getenv("DEEPGRAM_API_KEY"))

    language_map = {
        "en": "en-US",
        "es": "es-419",
        "fr": "fr-FR",
        "de": "de-DE",
        "ja": "ja-JP",
        "zh": "zh-CN",
    }

    model_language = language_map.get(language, "en-US")

    options = {
        "model": "nova-2",
        "language": model_language,
        "interim_results": True,
        "smart_format": enable_punctuation,
        "punctuate": enable_punctuation,
        "encoding": "linear16",
        "sample_rate": 16000,
        "channels": 1,
    }

    connection = await dg_client.transcription.live(options)
    return connection


async def stream_with_settings(
    audio_source, language: str = "en", punctuation: bool = True
):
    connection = await start_streaming_recognizer(language, punctuation)

    async def send_audio():
        async for chunk in audio_source:
            await connection.send(chunk)

    async def receive_transcripts():
        async for message in connection:
            if "channel" in message:
                for alternative in message["channel"]["alternatives"]:
                    if "transcript" in alternative:
                        transcript = alternative["transcript"]
                        if transcript:
                            is_final = message.get("is_final", False)
                            yield {
                                "transcript": transcript,
                                "is_final": is_final,
                                "language": language,
                                "has_punctuation": punctuation,
                            }

    send_task = asyncio.create_task(send_audio())

    try:
        async for result in receive_transcripts():
            yield result
    finally:
        send_task.cancel()
        try:
            await send_task
        except asyncio.CancelledError:
            pass
        await connection.finish()


class TestAudioSource:
    def __init__(self, duration_seconds=3, sample_rate=16000):
        self.duration = duration_seconds
        self.sample_rate = sample_rate
        self.chunk_size = 1024
        self.total_chunks = (duration_seconds * sample_rate) // self.chunk_size

    async def __aiter__(self):
        for i in range(self.total_chunks):
            yield b"\x00" * self.chunk_size
            await asyncio.sleep(0.01)


async def example_multilingual():
    print("Testing English with punctuation...")
    source = TestAudioSource(duration_seconds=2)

    async for result in stream_with_settings(source, language="en", punctuation=True):
        status = "FINAL" if result["is_final"] else "INTERIM"
        print(f"{status} [{result['language']}]: {result['transcript']}")

    print("\nTesting Spanish with punctuation...")
    source = TestAudioSource(duration_seconds=2)

    async for result in stream_with_settings(source, language="es", punctuation=True):
        status = "FINAL" if result["is_final"] else "INTERIM"
        print(f"{status} [{result['language']}]: {result['transcript']}")


if __name__ == "__main__":
    asyncio.run(example_multilingual())
