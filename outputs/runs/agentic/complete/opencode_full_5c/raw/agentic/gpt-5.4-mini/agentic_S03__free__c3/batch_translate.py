from openai import OpenAI
from translation_client import TranslationConfig, build_instruction, get_client
from translation_models import normalize_text_list


def batch_translate(texts, source_language='auto', target_language='en'):
    config = TranslationConfig.from_env()
    client: OpenAI = get_client(config.api_key)
    normalized = normalize_text_list(list(texts))
    results = []
    for text in normalized:
        response = client.responses.create(
            model=config.model,
            input=[
                {'role': 'system', 'content': build_instruction(source_language, target_language)},
                {'role': 'user', 'content': text},
            ],
        )
        results.append(response.output_text.strip())
    return results
