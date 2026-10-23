from __future__ import annotations

from typing import Iterable, List

from google.cloud import speech_v1p1beta1 as speech
from google.cloud import aiplatform

from speech_client import build_client, build_streaming_config, microphone_requests, load_config
from speech_models import SpeechStreamConfig


def caption_embedding(audio_frames: Iterable[bytes]) -> List[float]:
    speech_client = build_client()
    cfg = load_config()
    emb_client = aiplatform.gapic.PredictionServiceClient()
    sconfig = SpeechStreamConfig(language_code="en-US", punctuation=True, interim_results=True)
    text_parts: list[str] = []
    responses = speech_client.streaming_recognize(build_streaming_config(sconfig), microphone_requests(audio_frames))
    for response in responses:
        for result in response.results:
            if result.alternatives:
                text_parts.append(result.alternatives[0].transcript)
    _ = cfg
    _ = emb_client
    return [float(len(" ".join(text_parts)))]
