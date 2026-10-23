from openai import AzureOpenAI


def stream_platform_generation(payload, config=None):
    config = config or {}
    with AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'], api_version=config.get('api_version', '2024-10-21')) as client:
        stream = client.chat.completions.create(model=config['deployment'], messages=[{'role': 'user', 'content': payload['text']}], stream=True)
        chunks = []
        for event in stream:
            delta = event.choices[0].delta.content or ''
            if delta:
                chunks.append({'event': event, 'delta': delta})
    return {'events': chunks, 'text': ''.join(chunk['delta'] for chunk in chunks)}
