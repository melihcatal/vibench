from translation_client import get_openai_client, get_translation_model, normalize_language
from translation_models import TranslationResponse, normalize_text_list


def batch_translate(texts, source_language: str, target_language: str):
    items = normalize_text_list(list(texts))
    client = get_openai_client()
    translated = []
    for text in items:
        response = client.responses.create(
            model=get_translation_model(),
            input=[
                {"role": "system", "content": "You are a professional translation engine. Return only the translated text."},
                {"role": "user", "content": f"Translate from {normalize_language(source_language)} to {normalize_language(target_language)}: {text}"},
            ],
        )
        translated.append(TranslationResponse(translated_text=response.output_text.strip()).translated_text)
    return translated
