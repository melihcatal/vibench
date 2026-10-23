from translation_client import build_translation_messages, get_openai_client, get_translation_deployment
from translation_models import TranslationRequest, TranslationResult, normalize_text


def translate_text(text: str, source_language: str | None = None, target_language: str = "en") -> TranslationResult:
    request = TranslationRequest(text=normalize_text(text), source_language=source_language, target_language=target_language)
    client = get_openai_client()
    response = client.chat.completions.create(model=get_translation_deployment(), messages=build_translation_messages(request.text, request.source_language, request.target_language))
    translated_text = response.choices[0].message.content or ""
    return TranslationResult(translated_text=translated_text, source_language=request.source_language, target_language=request.target_language, raw=response.model_dump())
