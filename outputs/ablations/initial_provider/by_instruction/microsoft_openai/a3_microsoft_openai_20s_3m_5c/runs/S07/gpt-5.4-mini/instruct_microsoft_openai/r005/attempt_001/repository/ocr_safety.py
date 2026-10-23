import os
from openai import AzureOpenAI

from document_client import require_azure_openai_config


def check_ocr_safety(text: str) -> str:
    config = require_azure_openai_config()
    client = AzureOpenAI(api_key=config.azure_api_key, azure_endpoint=config.azure_endpoint, api_version=config.azure_api_version)
    model = os.getenv("AZURE_OPENAI_SAFETY_MODEL", "gpt-4o-mini")
    response = client.chat.completions.create(model=model, messages=[{"role": "system", "content": "Assess the document text for unsafe content and return a short verdict."}, {"role": "user", "content": text}])
    return response.choices[0].message.content or ""
