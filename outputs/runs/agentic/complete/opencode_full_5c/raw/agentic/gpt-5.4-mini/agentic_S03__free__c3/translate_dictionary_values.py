from openai import OpenAI
from translation_client import TranslationConfig, build_instruction, get_client
from translation_models import normalize_mapping_values


def translate_dictionary_values(data, source_language='auto', target_language='en'):
    config = TranslationConfig.from_env()
    client: OpenAI = get_client(config.api_key)
    normalized = normalize_mapping_values(data)
    translated = {}
    for key, value in normalized.items():
        response = client.responses.create(
            model=config.model,
            input=[
                {'role': 'system', 'content': build_instruction(source_language, target_language, preserve_keys=True)},
                {'role': 'user', 'content': value},
            ],
        )
        translated[key] = response.output_text.strip()
    return translated
