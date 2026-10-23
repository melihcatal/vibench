import os
from typing import Optional

from google.cloud import translate_v2 as translate
from vision_models import ImageDescription


def translate_alt_text(
    description: ImageDescription,
    target_language: str = "es",
    project_id: Optional[str] = None,
) -> str:
    """
    Translates generated image descriptions using Google Cloud Translation.

    Args:
        description: Image description to translate.
        target_language: Target language code (e.g., 'es' for Spanish).
        project_id: Google Cloud project ID. If None, uses GOOGLE_APPLICATION_CREDENTIALS.

    Returns:
        Translated description text.
    """
    client = translate.Client()

    if not project_id:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    try:
        result = client.translate(
            description.description,
            target_language=target_language,
            project_id=project_id,
        )
        return result["translatedText"]

    except Exception as e:
        raise Exception(f"Google Cloud Translation error: {e}")
