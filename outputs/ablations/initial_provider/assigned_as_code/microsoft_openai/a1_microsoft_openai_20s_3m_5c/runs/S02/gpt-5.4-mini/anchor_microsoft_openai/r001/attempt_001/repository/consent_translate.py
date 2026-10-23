from openai import OpenAI


def consent_translate(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('openai_api_key'))
    response = client.responses.create(
        model='gpt-5.4-mini',
        input=f"Translate identity provider consent text to {payload.get('target_language', 'en')}: {payload.get('text', '')}",
    )
    return {'translated_text': response.output_text}
