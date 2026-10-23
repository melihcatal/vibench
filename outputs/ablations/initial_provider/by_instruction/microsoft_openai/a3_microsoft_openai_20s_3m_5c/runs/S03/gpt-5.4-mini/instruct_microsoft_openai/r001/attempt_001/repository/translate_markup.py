from translation_client import build_translation_instruction, get_openai_client, get_translation_model
from translation_models import TranslationResult


def translate_markup(text: str, source_language: str | None = None, target_language: str = "en") -> TranslationResult:
    client = get_openai_client()
    response = client.responses.create(
        model=get_translation_model(),
        input=[
            {
                "role": "system",
                "content": build_translation_instruction(source_language, target_language, preserve_tags=True),
            },
            {"role": "user", "content": text},
        ],
    )
    return TranslationResult(
        translated_text=response.output_text,
        source_language=source_language,
        target_language=target_language,
        metadata={"provider": "openai", "model": get_translation_model(), "preserve_tags": True},
    )
