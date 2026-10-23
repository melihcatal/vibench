from openai import OpenAI


def payload_translate(payload_text, target_language, config=None):
    client = OpenAI(api_key=(config or {}).get('api_key'))
    response = client.responses.create(
        model='gpt-5.4-mini',
        input=f'Translate the following customer-facing message to {target_language}: {payload_text}',
    )
    return {'translated_text': response.output_text}
