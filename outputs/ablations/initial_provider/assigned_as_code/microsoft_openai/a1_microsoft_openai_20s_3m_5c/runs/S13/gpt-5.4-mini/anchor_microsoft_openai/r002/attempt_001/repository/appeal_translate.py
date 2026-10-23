from openai import OpenAI


def appeal_translate(payload, config=None):
    client = OpenAI(api_key=(config or {}).get('api_key'))
    response = client.responses.create(model='gpt-4.1-mini', input=f"Translate this appeal for human review: {payload['text']}")
    return {'translation': response.output_text}
