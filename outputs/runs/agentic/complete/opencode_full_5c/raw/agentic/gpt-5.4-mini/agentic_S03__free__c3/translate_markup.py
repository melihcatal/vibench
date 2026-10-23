from openai import OpenAI
from translation_client import TranslationConfig, build_instruction, get_client
from translation_models import normalize_text


def translate_markup(markup, source_language='auto', target_language='en'):
    config = TranslationConfig.from_env()
    client: OpenAI = get_client(config.api_key)
    response = client.responses.create(
        model=config.model,
        input=[
            {'role': 'system', 'content': build_instruction(source_language, target_language, preserve_markup=True)},
            {'role': 'user', 'content': normalize_text(markup)},
        ],
    )
    return response.output_text.strip()
