from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TextTranslationClient

from document_client import load_config


def ocr_translate(
    text: str, target_language: str = "en", source_language: str | None = None
) -> str:
    config = load_config()
    client = TextTranslationClient(
        endpoint=config.endpoint or "",
        credential=AzureKeyCredential(config.api_key or ""),
        region=config.project_id,
    )
    response = client.translate(
        content=[text], to=[target_language], from_parameter=source_language
    )  # type: ignore[arg-type]
    return response[0].translations[0].text if response else ""
