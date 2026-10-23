from translation_client import build_translation_instruction, get_openai_client, get_translation_model
from translation_models import TranslationResult, normalize_text_list


def batch_translate(texts, source_language: str | None = None, target_language: str = "en"):
    client = get_openai_client()
    normalized = normalize_text_list(list(texts))
    results = []
    for text in normalized:
        response = client.responses.create(
            model=get_translation_model(),
            input=[
                {
                    "role": "system",
                    "content": build_translation_instruction(source_language, target_language),
                },
                {"role": "user", "content": text},
            ],
        )
        results.append(
            TranslationResult(
                translated_text=response.output_text,
                source_language=source_language,
                target_language=target_language,
                metadata={"provider": "openai", "model": get_translation_model(), "index": len(results)},
            )
        )
    return results
