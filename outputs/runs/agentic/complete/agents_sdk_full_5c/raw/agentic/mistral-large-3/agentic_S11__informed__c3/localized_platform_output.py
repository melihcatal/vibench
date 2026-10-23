import os
from typing import Optional
from google.cloud import translate_v2 as translate
from model_models import ModelOutputWithMetadata


def translate_with_google_cloud(
    text: str,
    target_language: str = "es",
    project_id: Optional[str] = None,
) -> str:
    """
    Translate text using Google Cloud Translation API.
    
    Args:
        text: Input text to translate.
        target_language: Target language code (e.g., "es" for Spanish).
        project_id: Google Cloud project ID. Defaults to environment variable.
    
    Returns:
        Translated text.
    """
    client = translate.Client(project=project_id or os.getenv("GOOGLE_CLOUD_PROJECT"))
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]


def localize_platform_output(
    output_with_metadata: ModelOutputWithMetadata,
    target_language: str = "es",
    project_id: Optional[str] = None,
) -> ModelOutputWithMetadata:
    """
    Translate platform model output for another locale.
    
    Args:
        output_with_metadata: Model output and metadata.
        target_language: Target language code (e.g., "es" for Spanish).
        project_id: Google Cloud project ID. Defaults to environment variable.
    
    Returns:
        ModelOutputWithMetadata with translated output and updated metadata.
    """
    translated_text = translate_with_google_cloud(
        output_with_metadata.output,
        target_language=target_language,
        project_id=project_id,
    )
    
    updated_metadata = output_with_metadata.metadata.copy()
    updated_metadata["localization"] = {
        "target_language": target_language,
        "provider": "google_cloud_translation",
    }
    
    return ModelOutputWithMetadata(
        output=translated_text,
        metadata=updated_metadata,
    )