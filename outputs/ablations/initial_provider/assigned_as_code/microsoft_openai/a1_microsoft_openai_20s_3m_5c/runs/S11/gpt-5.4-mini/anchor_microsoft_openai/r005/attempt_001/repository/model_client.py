from openai import AzureOpenAI


def load_platform_config(config=None):
    config = dict(config or {})
    config.setdefault('api_version', '2024-10-21')
    return config


def build_platform_client(config=None):
    config = load_platform_config(config)
    return AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'], api_version=config['api_version'])


def get_platform_deployment(config=None):
    config = load_platform_config(config)
    return config['deployment']
