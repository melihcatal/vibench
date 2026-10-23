from openai import AzureOpenAI


def platform_output_safety(payload, config=None):
    config = config or {}
    text = payload['text']
    with AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'], api_version=config.get('api_version', '2024-10-21')) as client:
        response = client.chat.completions.create(model=config['deployment'], messages=[{'role': 'system', 'content': 'Classify whether the user text contains unsafe content. Return safe or unsafe.'}, {'role': 'user', 'content': text}])
    verdict = response.choices[0].message.content or ''
    return {'text': text, 'safety_verdict': verdict, 'model': response.model}
