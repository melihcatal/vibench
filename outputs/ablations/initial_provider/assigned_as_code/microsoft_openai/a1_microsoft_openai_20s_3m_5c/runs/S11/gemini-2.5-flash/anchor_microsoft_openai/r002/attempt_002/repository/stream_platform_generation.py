from openai import AzureOpenAI


def stream_platform_generation(payload, config=None):
    config = config or {}
    with AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'],
                      api_version=config.get('api_version', '2024-10-21')) as client:
        stream = client.chat.completions.create(model=config['deployment'],
            messages=[{'role': 'user', 'content': payload['text']}], stream=True)

        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content is not None:
                yield {
                    'text': chunk.choices[0].delta.content,
                    'raw_response': chunk.model_dump_json()
                }
