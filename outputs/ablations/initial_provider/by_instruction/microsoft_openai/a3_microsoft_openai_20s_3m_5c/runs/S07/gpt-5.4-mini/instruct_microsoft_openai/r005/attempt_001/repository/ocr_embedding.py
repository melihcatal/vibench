import os
from openai import AzureOpenAI

from document_client import require_azure_openai_config


def embed_ocr_sections(sections: list[str]) -> list[list[float]]:
    config = require_azure_openai_config()
    client = AzureOpenAI(api_key=config.azure_api_key, azure_endpoint=config.azure_endpoint, api_version=config.azure_api_version)
    model = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")
    vectors = []
    for section in sections:
        response = client.embeddings.create(model=model, input=section)
        vectors.append(response.data[0].embedding)
    return vectors
