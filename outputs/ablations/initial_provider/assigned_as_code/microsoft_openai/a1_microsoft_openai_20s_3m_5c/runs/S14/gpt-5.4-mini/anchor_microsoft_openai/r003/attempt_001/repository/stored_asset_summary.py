from openai import AzureOpenAI


def stored_asset_summary(payload, config=None):
    config = config or {}
    client = AzureOpenAI(azure_endpoint=config['openai_endpoint'], api_key=config['openai_key'], api_version=config.get('openai_api_version', '2024-02-15-preview'))
    response = client.chat.completions.create(
        model=config['openai_deployment'],
        messages=[{'role': 'system', 'content': 'Summarize the provided asset content.'}, {'role': 'user', 'content': payload['text']}],
    )
    return {'summary': response.choices[0].message.content}
