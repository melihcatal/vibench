from openai import OpenAI


def moderation_summary(payload, config=None):
    client = OpenAI(api_key=(config or {}).get('api_key'))
    text = payload['text']
    response = client.responses.create(model='gpt-4.1-mini', input=f'Summarize moderation decision context: {text}')
    return {'summary': response.output_text}
