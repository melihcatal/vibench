from openai import AzureOpenAI


def collect_platform_metadata(payload, config=None):
    config = config or {}
    with AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'], api_version=config.get('api_version', '2024-10-21')) as client:
        response = client.chat.completions.create(model=config['deployment'], messages=[{'role': 'user', 'content': payload['text']}])
    choice = response.choices[0].message.content or ''
    usage = response.usage
    return {'text': choice, 'model': response.model, 'usage': {'input_tokens': getattr(usage, 'prompt_tokens', None), 'output_tokens': getattr(usage, 'completion_tokens', None), 'total_tokens': getattr(usage, 'total_tokens', None)}, 'resource_id': config['deployment']}
