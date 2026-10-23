from __future__ import annotations

from typing import Iterable, Iterator, Tuple

from google.cloud import speech_v1p1beta1 as speech
from google.cloud import language_v1

from speech_client import build_client, build_streaming_config, microphone_requests
from speech_models import SpeechStreamConfig


def live_caption_safety(audio_frames: Iterable[bytes]) -> Iterator[Tuple[str, float]]:
    speech_client = build_client()
    nlp_client = language_v1.LanguageServiceClient()
    config = SpeechStreamConfig(language_code="en-US", punctuation=True, interim_results=True)
    responses = speech_client.streaming_recognize(build_streaming_config(config), microphone_requests(audio_frames))
    for response in responses:
        for result in response.results:
            if not result.alternatives:
                continue
            text = result.alternatives[0].transcript
            doc = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
            sentiment = nlp_client.analyze_sentiment(request={"document": doc})
            yield text, sentiment.document_sentiment.score
