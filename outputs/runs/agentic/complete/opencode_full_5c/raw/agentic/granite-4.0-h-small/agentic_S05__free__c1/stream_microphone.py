import asyncio
import audioop
import json
import aioconsole

from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_google_client

# Constants
LANGUAGE_CODE = "en-US"
ENCODING = speech.RecognitionConfig.AudioEncoding.LINEAR16
SAMPLE_RATE = 16000


# Configure microphone stream
async def microphone_generator():
    # Use aioconsole to capture raw PCM audio from the default microphone
    async with aioconsole.AioStreamReader() as stream:
        while True:
            data = await stream.readline()  # binary bytes
            if not data:
                break
            yield data


def chunk_to_recognition_chunk(chunk: bytes):
    # Prepare a streaming recognize request chunk
    return {
        "audio_content": chunk,
    }


async def main():
    client = get_google_client()
    config = speech.RecognitionConfig(
        encoding=ENCODING,
        sample_rate_hertz=SAMPLE_RATE,
        language_code=LANGUAGE_CODE,
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    requests = []
    async for audio in microphone_generator():
        requests.append(speech.StreamingRecognizeRequest(audio=audio))
        if audio and audioop.len(audio) >= 320:  # approx 20 ms chunk for 16kHz 16-bit
            await client.streaming_recognize(streaming_config, requests)
            requests = []
    # Finish stream
    await client.streaming_recognize(streaming_config, requests)


if __name__ == "__main__":
    asyncio.run(main())
