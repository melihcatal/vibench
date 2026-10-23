from typing import AsyncIterator, Iterator

from speech_client import build_client, default_config, streaming_config
from speech_models import event_from_result


def stream_chunks(chunks: AsyncIterator[bytes]) -> Iterator[str]:
    client = build_client()
    cfg = default_config()

    async def request_iter():
        async for chunk in chunks:
            yield {"audio_content": chunk}

    for response in client.streaming_recognize(streaming_config(cfg), request_iter()):
        for result in response.results:
            event = event_from_result(result, cfg.language_code)
            if event.text:
                yield event.text
