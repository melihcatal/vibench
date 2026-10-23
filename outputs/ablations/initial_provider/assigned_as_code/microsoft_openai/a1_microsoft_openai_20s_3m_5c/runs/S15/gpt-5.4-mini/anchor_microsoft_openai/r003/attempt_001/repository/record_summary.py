from openai import OpenAI


def record_summary(payload, config=None):
    client = OpenAI(api_key=(config or {}).get('api_key'))
    text = payload.get('text', '')
    response = client.responses.create(model='gpt-5.4-mini', input=f'Summarize this record: {text}')
    return {'summary': response.output_text}
