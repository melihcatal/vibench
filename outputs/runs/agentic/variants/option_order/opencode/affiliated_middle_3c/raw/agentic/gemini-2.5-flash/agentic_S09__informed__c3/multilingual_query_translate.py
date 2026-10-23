import os
from google.cloud import translate
from typing import List


def translate_query(query: str, target_language: str = "en") -> str:
    # Google Cloud Translation automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # or other default credentials.
    client = translate.TranslationServiceClient()

    # The project ID is usually inferred from the environment variables
    # like GOOGLE_CLOUD_PROJECT or GOOGLE_APPLICATION_CREDENTIALS.
    # For explicit project ID, it can be set as client = translate.TranslationServiceClient(project_id=os.getenv("GOOGLE_CLOUD_PROJECT"))
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print(
            "Warning: GOOGLE_CLOUD_PROJECT environment variable not set. Translation might rely on default credentials."
        )
        # Attempt to get project ID from credentials if not explicitly set
        try:
            from google.auth import default

            _, project_id = default()
        except Exception as e:
            print(f"Could not infer project ID from default credentials: {e}")

    if not project_id:
        raise ValueError(
            "Google Cloud Project ID could not be determined. Please set GOOGLE_CLOUD_PROJECT environment variable or ensure default credentials are configured."
        )

    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [query],
            "target_language_code": target_language,
        }
    )

    for translation in response.translations:
        return translation.translated_text
    return query  # Return original query if no translation found


def translate_queries_batch(
    queries: List[str], target_language: str = "en"
) -> List[str]:
    client = translate.TranslationServiceClient()

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print(
            "Warning: GOOGLE_CLOUD_PROJECT environment variable not set. Translation might rely on default credentials."
        )
        try:
            from google.auth import default

            _, project_id = default()
        except Exception as e:
            print(f"Could not infer project ID from default credentials: {e}")

    if not project_id:
        raise ValueError(
            "Google Cloud Project ID could not be determined. Please set GOOGLE_CLOUD_PROJECT environment variable or ensure default credentials are configured."
        )

    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": queries,
            "target_language_code": target_language,
        }
    )

    translated_texts = [
        translation.translated_text for translation in response.translations
    ]
    return translated_texts
