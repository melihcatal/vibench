from openai import AzureOpenAI

from storage_client import get_azure_openai_client, load_storage_config


def stored_document_ocr(object_name, extracted_text):
    config = load_storage_config()
    client: AzureOpenAI = get_azure_openai_client(config)
    response = client.responses.create(
        model=config.azure_openai_deployment,
        input=f"Extract OCR from {object_name}: {extracted_text}",
    )
    return response.output_text
