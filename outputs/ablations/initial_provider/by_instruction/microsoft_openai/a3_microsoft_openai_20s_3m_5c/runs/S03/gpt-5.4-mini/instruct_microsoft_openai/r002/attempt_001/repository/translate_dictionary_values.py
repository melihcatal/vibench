from openai import OpenAI

from translation_client import get_translation_model, normalize_language


def translate_dictionary_values(data, source_language: str, target_language: str):
    client = OpenAI()
    result = {}
    for key, value in data.items():
        response = client.responses.create(
            model=get_translation_model(),
            input=[
                {"role": "system", "content": "Translate dictionary values while preserving keys."},
                {"role": "user", "content": f"Translate from {normalize_language(source_language)} to {normalize_language(target_language)}: {value}"},
            ],
        )
        result[key] = response.output_text.strip()
    return result
