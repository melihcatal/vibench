from openai import AzureOpenAI

def select_platform_resource(config):
    client = AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'], api_version=config.get('api_version', '2024-10-21'))
    deployments = client.deployments.list()
    for deployment in deployments:
        if deployment.model == config['model']:
            return deployment.id
    raise ValueError('Model not found')