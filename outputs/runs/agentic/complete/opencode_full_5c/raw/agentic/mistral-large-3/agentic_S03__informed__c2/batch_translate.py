from typing import List
from translation_client import GoogleTranslationClient
from translation_models import TranslationRequest, normalize_language_code


def batch_translate(
    texts: List[str], target_language: str, source_language: str = None
) -> List[str]:
    client = GoogleTranslationClient()
    target_language = normalize_language_code(target_language)
    source_language = (
        normalize_language_code(source_language) if source_language else None
    )

    requests = [
        TranslationRequest(
            text=text, target_language=target_language, source_language=source_language
        )
        for text in texts
    ]
    responses = client.batch_translate_text(requests)
    return [response.translated_text for response in responses]
