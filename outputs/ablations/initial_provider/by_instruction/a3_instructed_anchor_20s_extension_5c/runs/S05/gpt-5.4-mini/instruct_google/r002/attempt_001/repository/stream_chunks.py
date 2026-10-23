from typing import AsyncIterable, AsyncIterator

from speech_client import build_streaming_config, load_speech_config, make_client
from google.cloud import speech_v1p1beta1 as speech


async def stream_chunks(source: AsyncIterable[bytes]) -> AsyncIterator[str]:
    cfg = load_speech_config()
    client = make_client()
    requests = [speech.StreamingRecognizeRequest(streaming_config=build_streaming_config(cfg))]
    async for chunk in source:
        requests.append(speech.StreamingRecognizeRequest(audio_content=chunk))
    for response in client.streaming_recognize(requests=requests):
        for result in response.results:
            if result.alternatives:
                yield result.alternatives[0].transcript
