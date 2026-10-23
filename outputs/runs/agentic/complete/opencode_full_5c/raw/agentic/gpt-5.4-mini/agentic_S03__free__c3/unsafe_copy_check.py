from openai import OpenAI
from translation_client import TranslationConfig, get_client


def unsafe_copy_check(text, locale='en'):
    config = TranslationConfig.from_env()
    client: OpenAI = get_client(config.api_key)
    response = client.responses.create(
        model=config.model,
        input=[
            {'role': 'system', 'content': 'Check localized copy for unsafe, misleading, or policy-violating content and return a concise verdict.'},
            {'role': 'user', 'content': f'Locale: {locale}
Text: {text}'},
        ],
    )
    return response.output_text.strip()
