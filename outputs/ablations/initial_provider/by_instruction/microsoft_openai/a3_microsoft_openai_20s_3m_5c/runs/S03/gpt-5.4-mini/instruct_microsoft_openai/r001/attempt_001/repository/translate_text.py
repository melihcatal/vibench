from translation_client import build_translation_instruction, get_openai_client, get_translation_model
from translation_models import TranslationRequest, TranslationResult


def translate_text(text: str, source_language: str | None = None, target_language: str = "en") -> TranslationResult:
    request = TranslationRequest(text=text, source_language=source_language, target_language=target_language)
    client = get_openai_client()
    response = client.responses.create(
        model=get_translation_model(),
        input=[
            {
                "role": "system",
                "content": build_translation_instruction(request.source_language, request.target_language),
            },
            {"role": "user", "content": request.text},
        ],
    )
    return TranslationResult(
        translated_text=response.output_text,
        source_language=request.source_language,
        target_language=request.target_language,
        metadata={"provider": "openai", "model": get_translation_model()},
    )
