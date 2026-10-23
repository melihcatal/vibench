from openai import AzureOpenAI


def collect_platform_metadata(payload, config=None):
    config = config or {}
    with AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'],
                      api_version=config.get('api_version', '2024-10-21')) as client:
        response = client.chat.completions.create(model=config['deployment'],
            messages=[{'role': 'user', 'content': payload['text']}])

    metadata = {
        'model': response.model,
        'prompt_tokens': response.usage.prompt_tokens,
        'completion_tokens': response.usage.completion_tokens,
        'total_tokens': response.usage.total_tokens,
        'finish_reason': response.choices[0].finish_reason
    }
    return {'text': response.choices[0].message.content or '', 'metadata': metadata}
