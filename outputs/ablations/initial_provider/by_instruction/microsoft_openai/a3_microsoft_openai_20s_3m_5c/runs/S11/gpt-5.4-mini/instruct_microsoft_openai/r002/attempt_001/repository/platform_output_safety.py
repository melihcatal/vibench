from openai import AzureOpenAI

from model_client import load_platform_config


def platform_output_safety(text: str) -> bool:
    config = load_platform_config()
    client = AzureOpenAI(azure_endpoint=config.endpoint, api_key=config.api_key, api_version=config.api_version)
    result = client.moderations.create(input=text)
    return not any(flagged for item in result.results for flagged in (item.flagged,))
