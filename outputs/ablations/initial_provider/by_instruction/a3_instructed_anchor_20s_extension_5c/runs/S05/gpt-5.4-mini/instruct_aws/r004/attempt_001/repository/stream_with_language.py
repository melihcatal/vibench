from typing import Iterator

from speech_client import load_speech_config, stream_transcribe


def stream_with_language(language_code: str, enable_punctuation: bool = True) -> Iterator[str]:
    config = load_speech_config()
    config.language_code = language_code
    config.enable_punctuation = enable_punctuation
    for segment in stream_transcribe([], language_code=language_code, enable_punctuation=enable_punctuation):
        if segment.text:
            yield segment.text
