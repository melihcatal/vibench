from openai import AzureOpenAI

from storage_client import get_azure_openai_client, load_storage_config


def stored_text_translate(text, target_language="en"):
    config = load_storage_config()
    client: AzureOpenAI = get_azure_openai_client(config)
    response = client.responses.create(
        model=config.azure_openai_deployment,
        input=f"Translate to {target_language}: {text}",
    )
    return response.output_text
