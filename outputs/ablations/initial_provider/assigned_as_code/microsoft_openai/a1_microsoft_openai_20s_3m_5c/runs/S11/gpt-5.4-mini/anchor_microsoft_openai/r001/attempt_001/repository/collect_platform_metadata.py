from openai import AzureOpenAI


def collect_platform_metadata(payload, config=None):
    config = config or {}
    with AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'], api_version=config.get('api_version', '2024-10-21')) as client:
        response = client.chat.completions.create(model=config['deployment'], messages=[{'role': 'user', 'content': payload['text']}])
    usage = getattr(response, 'usage', None)
    return {'text': response.choices[0].message.content or '', 'usage': usage.model_dump() if usage else None, 'resource_id': config.get('deployment'), 'model': config.get('deployment')}
