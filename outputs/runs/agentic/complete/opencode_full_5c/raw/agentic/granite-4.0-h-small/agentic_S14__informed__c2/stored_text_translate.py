import os
from typing import Optional
from .storage_client import StorageClient
from .storage_models import GenericObjectMetadata


def translate_extracted_text(
    provider: str, source_lang: str, target_lang: str, text: str
) -> str:
    """
    Translate text extracted from a stored document using a hosted translation API.

    Returns the translated string.
    """
    # Using Alibaba Cloud Machine Translation as an example provider
    import alibabacloud_alimt  # type: ignore[import]

    client = alibabacloud_alimt.AliyunClient(
        accessKeyId=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        accessKeySecret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    )
    response = client.translate(
        SourceText=text,
        SourceLanguage=source_lang,
        TargetLanguage=target_lang,
    )
    return response["Translated"]  # type: ignore[attr-defined]

    # If using a different provider, replace the SDK call accordingly.
    # Example for DeepL: deepL.translate(text, target_lang) after initializing the client.
