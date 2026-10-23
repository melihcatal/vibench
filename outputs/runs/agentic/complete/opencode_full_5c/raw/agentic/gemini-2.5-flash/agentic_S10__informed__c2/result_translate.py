import os
from typing import List, Union
from google.cloud import translate

from model_models import TranslateRequest, TranslateResponse


def translate_text(
    text: Union[str, List[str]], target_language: str, source_language: str = None
) -> TranslateResponse:
    """Translates generated model output using Google Cloud Translation."""
    # Google Cloud Translation client will use GOOGLE_APPLICATION_CREDENTIALS for authentication
    # Make sure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or authentication is handled by gcloud cli
    # Project ID is often automatically detected but can be specified if needed.
    # For this example, we assume default project ID from environment or gcloud config.

    client = translate.TranslationServiceClient()

    if isinstance(text, str):
        texts_to_translate = [text]
    else:
        texts_to_translate = text

    parent = (
        f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}"
        if os.getenv("GOOGLE_CLOUD_PROJECT")
        else None
    )  # Optional: Specify project ID

    response = client.translate_text(
        request={
            "parent": parent,  # Removed if not needed, or specify a valid project number.
            "contents": texts_to_translate,
            "target_language_code": target_language,
            "source_language_code": source_language,  # Optional
        }
    )

    return TranslateResponse.from_api_response(response)
