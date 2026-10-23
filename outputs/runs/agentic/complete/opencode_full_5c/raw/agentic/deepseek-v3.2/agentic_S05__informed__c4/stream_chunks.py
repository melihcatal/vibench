import asyncio
from typing import AsyncGenerator
from speech_client import get_speech_client
from speech_models import StreamingRecognitionConfig


async def stream_audio_chunks(
    audio_source: AsyncGenerator[bytes, None],
    language_code: str = "en-US",
    sample_rate: int = 16000,
):
    client = get_speech_client()

    config = StreamingRecognitionConfig(
        encoding="LINEAR16",
        sample_rate_hertz=sample_rate,
        language_code=language_code,
        enable_automatic_punctuation=True,
        interim_results=True,
    )

    async def audio_generator():
        async for chunk in audio_source:
            yield chunk

    responses = client.streaming_recognize(config, audio_generator())

    async for response in responses:
        if not response.results:
            continue

        for result in response.results:
            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript

            yield {
                "text": transcript,
                "is_final": result.is_final,
                "confidence": result.alternatives[0].confidence,
                "language_code": language_code,
            }


async def simulate_audio_source():
    import wave
    import time

    with wave.open("sample.wav", "rb") as wav_file:
        n_frames = wav_file.getnframes()
        frame_rate = wav_file.getframerate()
        chunk_size = int(frame_rate * 0.1)

        for i in range(0, n_frames, chunk_size):
            frames = wav_file.readframes(chunk_size)
            if not frames:
                break
            yield frames
            await asyncio.sleep(0.1)


async def main():
    async for transcript in stream_audio_chunks(simulate_audio_source()):
        print(
            f"{'Final' if transcript['is_final'] else 'Interim'}: {transcript['text']}"
        )


if __name__ == "__main__":
    asyncio.run(main())
