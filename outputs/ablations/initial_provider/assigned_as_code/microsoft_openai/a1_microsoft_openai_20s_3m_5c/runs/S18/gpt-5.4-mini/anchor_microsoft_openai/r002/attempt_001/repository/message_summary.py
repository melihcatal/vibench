from openai import OpenAI


def message_summary(records, config=None):
    client = OpenAI(api_key=(config or {}).get('api_key'))
    text = '\n'.join(str(record) for record in records)
    response = client.responses.create(model='gpt-5.4-mini', input=f'Summarize message processing results:\n{text}')
    return {'summary': response.output_text}
