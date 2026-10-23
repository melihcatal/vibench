import os
from openai import AzureOpenAI

from document_client import require_azure_openai_config


def translate_ocr_text(text: str, target_language: str = "en") -> str:
    config = require_azure_openai_config()
    client = AzureOpenAI(api_key=config.azure_api_key, azure_endpoint=config.azure_endpoint, api_version=config.azure_api_version)
    model = os.getenv("AZURE_OPENAI_TRANSLATION_MODEL", "gpt-4o-mini")
    response = client.chat.completions.create(model=model, messages=[{"role": "system", "content": f"Translate OCR text to {target_language}."}, {"role": "user", "content": text}])
    return response.choices[0].message.content or ""
