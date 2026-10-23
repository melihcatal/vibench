from invoke_platform_model import invoke_platform_model


def stream_platform_generation(payload, config):
    from openai import AzureOpenAI
    with AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'],
                     api_version=config.get('api_version', '2024-10-21')) as client:
        response = client.chat.completions.create(model=config['deployment'],
            messages=[{'role': 'user', 'content': payload['text']}], stream=True)
        for chunk in response:
            yield {'text': chunk.choices[0].delta.content or ''}
