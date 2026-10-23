from typing import List
from translation_client import DeepLTranslationClient
from translation_models import TranslationRequest


def batch_translate(
    texts: List[str], target_language: str, source_language: Optional[str] = None
) -> List[str]:
    """
    Translates a list of strings while preserving order using DeepL API.
    """
    client = DeepLTranslationClient()
    results = []
    for text in texts:
        request = TranslationRequest(
            text=text, target_language=target_language, source_language=source_language
        )
        response = client.translate_text(request)
        results.append(response.translated_text)
    return results
