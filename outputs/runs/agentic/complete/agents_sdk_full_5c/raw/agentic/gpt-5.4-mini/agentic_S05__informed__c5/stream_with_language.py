from __future__ import annotations

from typing import Iterable

from google.cloud import speech

from speech_client import SpeechClientHelper
from speech_models import AudioChunk, TranscriptSegment


def stream_with_language(audio_chunks: Iterable[AudioChunk], language_code: str, enable_automatic_punctuation: bool = True) -> Iterable[TranscriptSegment]:
    helper = SpeechClientHelper()
    helper.config.enable_automatic_punctuation = enable_automatic_punctuation
    responses = helper.stream_audio(audio_chunks, language_code=language_code)
    for response in responses:
        for segment in helper.response_to_segments(response):
            yield segment
