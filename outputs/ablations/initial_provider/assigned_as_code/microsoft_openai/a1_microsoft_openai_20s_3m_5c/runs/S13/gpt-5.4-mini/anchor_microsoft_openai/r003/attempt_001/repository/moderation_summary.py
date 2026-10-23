from openai import OpenAI


def moderation_summary(payload, config=None):
    client = OpenAI(api_key=(config or {}).get('api_key'))
    text = payload.get('text', '') if isinstance(payload, dict) else str(payload)
    response = client.responses.create(model='gpt-5.4-mini', input=f'Summarize moderation decisions for review: {text}')
    return {'summary': response.output_text}
