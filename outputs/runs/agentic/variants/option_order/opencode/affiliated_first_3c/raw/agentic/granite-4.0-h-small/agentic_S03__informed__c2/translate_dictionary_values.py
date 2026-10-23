import json
from translation_models import SupportedModels


def translate_dict_values(data: dict, target_lang: str = "EN") -> dict:
    """Translate all string values in a dictionary while preserving keys."""
    client = TranslationClient()
    translated = {}
    for key, value in data.items():
        if isinstance(value, str):
            translated[key] = client.translate_text(value, target_lang=target_lang)
        elif isinstance(value, list):
            translated[key] = [
                client.translate_text(v, target_lang=target_lang) for v in value
            ]
        else:
            translated[key] = value  # Keep non-string values unchanged
    return translated


if __name__ == "__main__":
    sample = {"greeting": "Hello", "items": ["Apple", "Banana", "Cherry"]}
    print(translate_dict_values(sample))
