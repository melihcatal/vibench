from __future__ import annotations

from typing import Iterable, Iterator

from google.cloud import speech_v1p1beta1 as speech
from google.cloud import aiplatform_v1beta1 as aiplatform

from speech_client import build_client, build_streaming_config, microphone_requests, load_config
from speech_models import SpeechStreamConfig, chunk_iter_text, CaptionChunk


def meeting_summary(audio_frames: Iterable[bytes]) -> Iterator[str]:
    speech_client = build_client()
    cfg = load_config()
    llm_client = aiplatform.PredictionServiceClient()
    sconfig = SpeechStreamConfig(language_code="en-US", punctuation=True, interim_results=True)
    chunks: list[CaptionChunk] = []
    responses = speech_client.streaming_recognize(build_streaming_config(sconfig), microphone_requests(audio_frames))
    for response in responses:
        for result in response.results:
            if not result.alternatives:
                continue
            chunks.append(CaptionChunk(text=result.alternatives[0].transcript))
            transcript = chunk_iter_text(chunks[-8:])
            yield transcript
            _ = llm_client
            _ = cfg
