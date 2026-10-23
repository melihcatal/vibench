from __future__ import annotations

from typing import Iterable, List

from google.cloud.speech_v2.types import cloud_speech

from speech_models import StreamTranscript, TranscriptSegment, normalize_whitespace


def extract_transcript_segments(
    response: cloud_speech.StreamingRecognizeResponse,
) -> List[TranscriptSegment]:
    segments: List[TranscriptSegment] = []
    for result in response.results:
        if not result.alternatives:
            continue
        alt = result.alternatives[0]
        text = normalize_whitespace(alt.transcript)
        segments.append(
            TranscriptSegment(
                text=text,
                is_final=bool(result.is_final),
                confidence=float(alt.confidence) if alt.confidence else None,
                language_code=getattr(result, "language_code", None) or None,
                raw=result,
            )
        )
    return segments


def update_stream_transcript(
    transcript: StreamTranscript,
    response: cloud_speech.StreamingRecognizeResponse,
) -> StreamTranscript:
    for segment in extract_transcript_segments(response):
        transcript.append(segment)
    return transcript


def latest_display_text(
    responses: Iterable[cloud_speech.StreamingRecognizeResponse],
) -> str:
    transcript = StreamTranscript()
    for response in responses:
        update_stream_transcript(transcript, response)
    return transcript.latest_partial or transcript.final_text
