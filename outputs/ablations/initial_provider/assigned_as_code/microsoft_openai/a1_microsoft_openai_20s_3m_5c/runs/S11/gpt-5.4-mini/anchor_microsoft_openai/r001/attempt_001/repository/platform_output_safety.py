from openai import AzureOpenAI


def platform_output_safety(payload, config=None):
    config = config or {}
    with AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'], api_version=config.get('api_version', '2024-10-21')) as client:
        response = client.moderations.create(model='omni-moderation-latest', input=payload['text'])
    result = response.results[0]
    return {'safe': not result.flagged, 'categories': result.categories.model_dump() if hasattr(result.categories, 'model_dump') else result.categories}
