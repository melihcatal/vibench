import os
import deepl
from speech_models import Transcript, TranscriptSegment
from typing import List


def translate_transcript(transcript: Transcript, target_lang: str = "ES") -> Transcript:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY required")
    translator = deepl.Translator(auth_key)
    translated_segments: List[TranscriptSegment] = []
    for seg in transcript.segments:
        result = translator.translate_text(seg.text, target_lang=target_lang)
        trans_seg = TranscriptSegment(
            start=seg.start,
            end=seg.end,
            text=result.text,
            speaker=seg.speaker,
            words=seg.words,
        )
        translated_segments.append(trans_seg)
    translated_text = " ".join(s.text for s in translated_segments)
    return Transcript(
        id=transcript.id, text=translated_text, segments=translated_segments
    )
