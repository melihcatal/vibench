from speech_client import post
from speech_models import TranslationRequest


def translate_transcript(text: str, target_language: str) -> dict:
    req = TranslationRequest(text=text, target_language=target_language)
    return post(
        "/translations",
        {
            "model": "gpt-4.1-mini",
            "input": req.text,
            "target_language": req.target_language,
        },
    )
