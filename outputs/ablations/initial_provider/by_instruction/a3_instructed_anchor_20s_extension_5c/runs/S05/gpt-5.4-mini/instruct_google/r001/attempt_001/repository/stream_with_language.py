from typing import Iterable, Iterator

from speech_client import build_client, default_config, streaming_config
from speech_models import event_from_result


def stream_with_language(chunks: Iterable[bytes], language_code: str, enable_punctuation: bool = True) -> Iterator[str]:
    client = build_client()
    cfg = default_config(language_code=language_code, enable_automatic_punctuation=enable_punctuation)
    requests = ({"audio_content": chunk} for chunk in chunks)
    for response in client.streaming_recognize(streaming_config(cfg), requests):
        for result in response.results:
            event = event_from_result(result, language_code)
            if event.text:
                yield event.text
