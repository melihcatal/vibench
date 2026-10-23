from openai import OpenAI


def stored_asset_summary(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config['openai_api_key'])
    response = client.responses.create(model='gpt-5.4-mini', input=payload['text'], instructions='Summarize the asset content concisely.')
    return {'summary': response.output_text}
