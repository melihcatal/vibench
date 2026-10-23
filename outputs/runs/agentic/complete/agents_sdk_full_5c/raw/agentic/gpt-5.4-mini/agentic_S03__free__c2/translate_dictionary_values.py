from typing import Any, Dict

from translation_client import create_openai_client, load_config
from translation_models import safe_dict_copy_with_values, normalize_translation_output


def translate_dictionary_values(data: Dict[str, Any], source_language: str, target_language: str) -> Dict[str, Any]:
    cfg = load_config()
    client = create_openai_client(cfg)
    translated_values: Dict[str, Any] = {}
    for key, value in data.items():
        if isinstance(value, str):
            prompt = (
                f"Translate from {source_language} to {target_language}. "
                f"Return only the translated text.\n\nText:\n{value}"
            )
            response = client.responses.create(model=cfg.model, input=prompt)
            translated_values[key] = normalize_translation_output(response.output_text)
        else:
            translated_values[key] = value
    return safe_dict_copy_with_values(data, translated_values)
