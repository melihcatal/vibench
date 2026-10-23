from typing import AsyncIterable, AsyncIterator

from google.cloud import speech

from speech_client import build_speech_client, streaming_config
from speech_models import segment_from_google_result


async def stream_audio_chunks(source: AsyncIterable[bytes], language_code: str = "en-US") -> AsyncIterator[str]:
    client = build_speech_client()
    config = streaming_config(language_code=language_code)

    async def requests():
        async for chunk in source:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    for response in client.streaming_recognize(config=config, requests=requests()):
        for result in response.results:
            segment = segment_from_google_result(result)
            if segment.text:
                yield segment.text
