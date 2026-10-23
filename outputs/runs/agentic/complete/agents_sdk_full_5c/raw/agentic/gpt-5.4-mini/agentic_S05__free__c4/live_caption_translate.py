from __future__ import annotations

from typing import Iterable, Iterator

from google.cloud import speech_v1p1beta1 as speech
from google.cloud import translate_v3 as translate

from speech_client import build_client, build_streaming_config, microphone_requests, load_config
from speech_models import SpeechStreamConfig


def live_caption_translate(audio_frames: Iterable[bytes], target_language_code: str = "es") -> Iterator[str]:
    speech_client = build_client()
    translate_client = translate.TranslationServiceClient()
    cfg = load_config()
    parent = f"projects/{cfg.project_id}/locations/global"
    sconfig = SpeechStreamConfig(language_code="en-US", punctuation=True, interim_results=True)
    responses = speech_client.streaming_recognize(build_streaming_config(sconfig), microphone_requests(audio_frames))
    for response in responses:
        for result in response.results:
            if not result.alternatives:
                continue
            text = result.alternatives[0].transcript
            translation = translate_client.translate_text(
                parent=parent,
                contents=[text],
                mime_type="text/plain",
                target_language_code=target_language_code,
            )
            yield translation.translations[0].translated_text
