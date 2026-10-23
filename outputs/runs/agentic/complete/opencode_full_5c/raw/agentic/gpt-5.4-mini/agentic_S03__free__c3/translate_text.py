import os
from translation_client import TranslationConfig, build_instruction, get_client
from translation_models import TranslationRequest, normalize_text


def translate_text(text: str, source_language: str = 'auto', target_language: str = 'en') -> str:
    config = TranslationConfig.from_env()
    client = get_client(config.api_key)
    request = TranslationRequest(text=normalize_text(text), source_language=source_language, target_language=target_language)
    response = client.responses.create(
        model=config.model,
        input=[
            {'role': 'system', 'content': build_instruction(request.source_language, request.target_language)},
            {'role': 'user', 'content': request.text},
        ],
    )
    return response.output_text.strip()


if __name__ == '__main__':
    import sys
    print(translate_text(sys.argv[1] if len(sys.argv) > 1 else ''))
