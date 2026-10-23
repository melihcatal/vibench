import os
import json
from typing import List
from translate import Translator

# Load API key for Alibaba Cloud Translation
ALIBABA_ACCESS_KEY_ID = os.getenv("ALIBABA_ACCESS_KEY_ID")
ALIBABA_ACCESS_KEY_SECRET = os.getenv("ALIBABA_ACCESS_KEY_SECRET")
TRANSLATOR = Translator(
    from_lang="en", to_lang="es"
)  # Example: translate English to Spanish


def translate_transcript_segments(transcript_segments: List[dict]) -> List[dict]:
    """Translate text of each segment using Alibaba Machine Translation."""
    translated_segments = []
    for seg in transcript_segments:
        translated = TRANSLATOR.translate(text=seg["text"])
        translated_segments.append(
            {"text": translated, "start": seg["start"], "end": seg["end"]}
        )
    return translated_segments


# Example usage:
# segments = [{'text': 'Hello world', 'start': 0, 'end': 1.2}, ...]
# translated = translate_transcript_segments(segments)
