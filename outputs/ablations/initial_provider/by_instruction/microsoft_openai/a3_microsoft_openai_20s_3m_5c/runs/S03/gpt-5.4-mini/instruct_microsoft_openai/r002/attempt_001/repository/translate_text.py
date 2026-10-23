from translation_client import get_openai_client, get_translation_model, normalize_language
from translation_models import TranslationRequest, TranslationResponse, normalize_text


def translate_text(text: str, source_language: str, target_language: str) -> str:
    request = TranslationRequest(
        text=normalize_text(text),
        source_language=normalize_language(source_language),
        target_language=normalize_language(target_language),
    )
    client = get_openai_client()
    response = client.responses.create(
        model=get_translation_model(),
        input=[
            {
                "role": "system",
                "content": "You are a professional translation engine. Return only the translated text.",
            },
            {
                "role": "user",
                "content": f"Translate from {request.source_language} to {request.target_language}: {request.text}",
            },
        ],
    )
    translated_text = response.output_text.strip()
    return TranslationResponse(translated_text=translated_text).translated_text
