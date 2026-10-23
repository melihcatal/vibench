import json
from typing import List, Dict
from speech_client import get_batch_speech_client
from speech_models import TranscriptionSegment, TranslationSegment


def translate_transcript(
    transcript: List[TranscriptionSegment],
    source_lang: str = "en",
    target_lang: str = "fr",
) -> List[TranslationSegment]:
    """Translate each text segment of a transcript to a target language.

    Returns a list of translated segments preserving start/end timestamps.
    """
    client = get_batch_speech_client()
    # Placeholder: assume provider offers a batch translation API
    # Example provider call:
    # translated = client.translate_batch(transcript, source_lang, target_lang)
    # Here we simulate a translation by prepending target language code.
    translated_segments = []
    for seg in transcript:
        translated_text = f"[{target_lang.upper()}] {seg['text']}"
        translated_segments.append(
            {
                "start": seg["start"],
                "end": seg["end"],
                "text": translated_text,
                "target_language": target_lang,
            }
        )
    return translated_segments


# Example invocation (commented out):
# if __name__ == "__main__":
#     segs = [{"start":0.0,"end":1.2,"text":"Hello"},{"start":1.2,"end":2.3,"text":"world"}]
#     trans = translate_transcript(segs)
#     print(json.dumps(trans, indent=2))
