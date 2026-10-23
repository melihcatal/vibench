from openai import AzureOpenAI

from storage_client import get_azure_openai_client, load_storage_config


def stored_asset_summary(content):
    config = load_storage_config()
    client: AzureOpenAI = get_azure_openai_client(config)
    response = client.responses.create(
        model=config.azure_openai_deployment,
        input=f"Summarize this asset content: {content}",
    )
    return response.output_text
