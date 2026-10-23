from translation_client import get_client
from translation_models import DictionaryTranslationRequest


def translate_dictionary_values(
    data: dict[str, str],
    source_lang: str = "auto",
    target_lang: str = "en",
    formality: str | None = None,
) -> dict[str, str]:
    client = get_client()
    request = DictionaryTranslationRequest(
        data=data,
        source_lang=source_lang,
        target_lang=target_lang,
        formality=formality,
    )
    response = client.translate_dictionary_values(request)
    return response.translated_data
