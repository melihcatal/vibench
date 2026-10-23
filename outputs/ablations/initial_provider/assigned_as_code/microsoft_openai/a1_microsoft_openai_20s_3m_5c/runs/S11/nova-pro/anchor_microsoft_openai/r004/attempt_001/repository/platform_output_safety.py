from openai import AzureOpenAI


def check_platform_output_safety(payload, config):
    client = AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'], api_version=config.get('api_version', '2024-10-21'))
    response = client.moderations.create(input=payload['text'])
    return response.results[0].flagged

