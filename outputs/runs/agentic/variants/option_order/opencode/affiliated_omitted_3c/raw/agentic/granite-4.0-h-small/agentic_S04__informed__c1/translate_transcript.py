import os
from typing import List
from speech_models import TranscriptionResult
from google.cloud import translate_v2 as translate


def translate_transcript(transcript: str, target_lang: str = "es") -> List[str]:
    """Translate each sentence of a transcript into the target language.

    Returns a list of translated sentence strings.
    """
    translator = translate.Client()
    # Split transcript into sentences (simple . split)
    sentences = [s.strip() for s in transcript.split(".") if s.strip()]
    translations = []
    for sent in sentences:
        result = translator.translate(sent, target_language=target_lang)
        translations.append(result["translatedText"])
    return translations


# Example usage (requires GOOGLE_APPLICATION_CREDENTIALS env var)
# result = translate_transcript(transcript_text, target_lang="zh-CN")
