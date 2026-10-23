from translation_client import get_client
from translation_models import BatchTranslationRequest


def batch_translate(
    texts: list[str],
    source_lang: str = "auto",
    target_lang: str = "en",
    formality: str | None = None,
) -> list[str]:
    client = get_client()
    request = BatchTranslationRequest(
        texts=texts,
        source_lang=source_lang,
        target_lang=target_lang,
        formality=formality,
    )
    response = client.batch_translate(request)
    return response.translated_texts()
