from openai import AzureOpenAI

from storage_models import extract_text_payload


def stored_asset_summary(payload, config=None):
    config = config or {}
    client = AzureOpenAI(azure_endpoint=config['openai_endpoint'], api_key=config['openai_key'], api_version=config.get('openai_api_version', '2024-06-01'))
    text = extract_text_payload(payload.get('text') or payload.get('content'))
    response = client.chat.completions.create(model=config['openai_deployment'], messages=[{'role': 'system', 'content': 'Summarize the provided asset content.'}, {'role': 'user', 'content': text}])
    return {'summary': response.choices[0].message.content}
