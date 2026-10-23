from openai import AzureOpenAI


def collect_platform_metadata(payload, config=None):
    config = config or {}
    with AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'], api_version=config.get('api_version', '2024-10-21')) as client:
        response = client.chat.completions.create(model=config['deployment'], messages=[{'role': 'user', 'content': payload['text']}])
    message = response.choices[0].message.content or ''
    usage = response.usage.model_dump() if getattr(response, 'usage', None) else {}
    return {'text': message, 'usage': usage, 'model': response.model, 'id': response.id}
