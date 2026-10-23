from openai import OpenAI

from storage_client import load_storage_config


def stored_asset_summary(payload, config=None):
    resolved = load_storage_config(config)
    client = OpenAI(api_key=resolved['openai_api_key'])
    completion = client.chat.completions.create(model=resolved.get('openai_model', 'gpt-5.4-mini'), messages=[{'role': 'user', 'content': payload['text']}])
    return {'summary': completion.choices[0].message.content}
