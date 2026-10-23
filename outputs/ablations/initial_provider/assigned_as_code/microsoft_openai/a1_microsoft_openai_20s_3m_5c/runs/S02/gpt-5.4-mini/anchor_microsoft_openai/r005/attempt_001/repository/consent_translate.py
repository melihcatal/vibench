from openai import OpenAI


def consent_translate(payload, config=None):
    payload = dict(payload or {})
    client = OpenAI(api_key=(config or {}).get('openai_api_key'))
    response = client.responses.create(
        model='gpt-5.4-mini',
        input=f"Translate this identity-provider consent copy to {payload.get('target_language', 'en')}: {payload.get('text', '')}",
    )
    return {'translation': response.output_text}
