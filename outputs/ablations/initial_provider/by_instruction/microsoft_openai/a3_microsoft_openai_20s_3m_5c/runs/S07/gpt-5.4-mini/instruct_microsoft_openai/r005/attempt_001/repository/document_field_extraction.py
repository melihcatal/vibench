import os
from openai import AzureOpenAI

from document_client import require_azure_openai_config


def extract_fields(normalized_text: str) -> str:
    config = require_azure_openai_config()
    client = AzureOpenAI(api_key=config.azure_api_key, azure_endpoint=config.azure_endpoint, api_version=config.azure_api_version)
    model = os.getenv("AZURE_OPENAI_FIELD_MODEL", "gpt-4o-mini")
    response = client.chat.completions.create(model=model, messages=[{"role": "system", "content": "Extract structured fields from normalized OCR text as concise JSON."}, {"role": "user", "content": normalized_text}])
    return response.choices[0].message.content or ""
