from google.cloud import translate_v2 as translate
from speech_models import TranscriptionResult, TranscriptSegment
from typing import List


def translate_transcript(
    transcript: TranscriptionResult, target_language: str
) -> List[TranscriptSegment]:
    """
    Translates completed transcript segments using Google Cloud Translation API.

    Args:
        transcript: TranscriptionResult containing segments to translate.
        target_language: Target language code (e.g., "es", "fr", "de").

    Returns:
        List of translated TranscriptSegment objects.
    """
    client = translate.Client()
    translated_segments = []

    for segment in transcript.segments:
        translation = client.translate(
            segment.text,
            target_language=target_language,
            source_language=transcript.language_code,
        )

        translated_segments.append(
            TranscriptSegment(
                text=translation["translatedText"],
                start_time=segment.start_time,
                end_time=segment.end_time,
                words=segment.words,
                speaker_tag=segment.speaker_tag,
            )
        )

    return translated_segments
