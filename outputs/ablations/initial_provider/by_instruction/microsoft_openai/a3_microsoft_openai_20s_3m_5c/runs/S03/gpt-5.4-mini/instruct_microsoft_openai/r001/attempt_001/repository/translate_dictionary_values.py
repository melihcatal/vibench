from translation_client import build_translation_instruction, get_openai_client, get_translation_model
from translation_models import TranslationResult, normalize_dict_values


def translate_dictionary_values(values, source_language: str | None = None, target_language: str = "en"):
    client = get_openai_client()
    normalized = normalize_dict_values(dict(values))
    translated = {}
    for key, value in normalized.items():
        response = client.responses.create(
            model=get_translation_model(),
            input=[
                {
                    "role": "system",
                    "content": build_translation_instruction(source_language, target_language),
                },
                {"role": "user", "content": value},
            ],
        )
        translated[key] = response.output_text
    return TranslationResult(
        translated_text=str(translated),
        source_language=source_language,
        target_language=target_language,
        metadata={"provider": "openai", "model": get_translation_model(), "keys": list(translated.keys())},
    )
