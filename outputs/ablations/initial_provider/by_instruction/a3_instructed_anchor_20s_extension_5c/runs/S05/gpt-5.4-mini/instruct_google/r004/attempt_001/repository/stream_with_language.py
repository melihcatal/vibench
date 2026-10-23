from typing import Iterable, Generator

from google.cloud import speech

from speech_client import build_speech_client, streaming_config
from speech_models import segment_from_google_result


def stream_with_language(audio_chunks: Iterable[bytes], language_code: str, enable_punctuation: bool = True) -> Generator[str, None, None]:
    client = build_speech_client()
    config = streaming_config(language_code=language_code, enable_punctuation=enable_punctuation)

    def requests():
        for chunk in audio_chunks:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    for response in client.streaming_recognize(config=config, requests=requests()):
        for result in response.results:
            segment = segment_from_google_result(result)
            if segment.text:
                yield segment.text
