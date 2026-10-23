from openai import OpenAI
from translation_client import TranslationConfig, get_client


def quality_summary(source_text, translated_text, issues=None):
    config = TranslationConfig.from_env()
    client: OpenAI = get_client(config.api_key)
    issue_text = ', '.join(issues or [])
    response = client.responses.create(
        model=config.model,
        input=[
            {'role': 'system', 'content': 'Summarize translation quality issues for localization review.'},
            {'role': 'user', 'content': f'Source: {source_text}
Translated: {translated_text}
Issues: {issue_text}'},
        ],
    )
    return response.output_text.strip()
