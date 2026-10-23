from deepgram import DeepgramClient, PrerecordedOptions
from speech_client import get_deepgram_client, DEEPGRAM_NOVA_MODEL
from speech_models import TranslationRequest, TranslationResult, TranscriptSegment


def translate_transcript(
    segments: list[TranscriptSegment],
    target_language: str,
    source_language: str | None = None,
) -> TranslationResult:
    client: DeepgramClient = get_deepgram_client()
    full_text = " ".join(seg.text for seg in segments)
    payload = {"text": full_text}
    options = PrerecordedOptions(
        model=DEEPGRAM_NOVA_MODEL,
        language=source_language or "en",
        detect_language=True,
    )
    response = client.listen.translate.v("1").translate_text(payload, options)
    translated_text = response.results.channels[0].alternatives[0].transcript
    translated_segments = [
        TranscriptSegment(
            text=translated_text,
            start=seg.start,
            end=seg.end,
            words=seg.words,
            speaker=seg.speaker,
        )
        for seg in segments
    ]
    return TranslationResult(
        segments=translated_segments, target_language=target_language
    )


def translate_segments_batch(
    segments: list[TranscriptSegment],
    target_language: str,
    source_language: str | None = None,
) -> TranslationResult:
    client: DeepgramClient = get_deepgram_client()
    translated = []
    for seg in segments:
        payload = {"text": seg.text}
        options = PrerecordedOptions(
            model=DEEPGRAM_NOVA_MODEL,
            language=source_language or "en",
        )
        response = client.listen.translate.v("1").translate_text(payload, options)
        translated_text = response.results.channels[0].alternatives[0].transcript
        translated.append(
            TranscriptSegment(
                text=translated_text,
                start=seg.start,
                end=seg.end,
                words=seg.words,
                speaker=seg.speaker,
            )
        )
    return TranslationResult(segments=translated, target_language=target_language)
