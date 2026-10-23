from openai import AzureOpenAI

from storage_client import get_azure_openai_client, load_storage_config


def asset_metadata_embedding(metadata, extracted_text):
    config = load_storage_config()
    client: AzureOpenAI = get_azure_openai_client(config)
    response = client.embeddings.create(
        model=config.azure_openai_deployment,
        input=[f"metadata: {metadata}", f"text: {extracted_text}"],
    )
    return [item.embedding for item in response.data]
