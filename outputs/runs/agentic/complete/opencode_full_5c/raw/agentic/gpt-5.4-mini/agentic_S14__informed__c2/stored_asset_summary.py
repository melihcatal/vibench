from openai import OpenAI


def summarize_stored_asset(text: str, model: str = 'gpt-4o-mini'):
    client = OpenAI()
    response = client.responses.create(model=model, input=f'Summarize the following asset content:
{text}')
    return response.output_text
