import os
from google.cloud import translate

def translate_appeal_text(text: str, target_language: str = "en") -> str:
    """
    Translates appeal text for review using Google Cloud Translation.
    """
    # Google Cloud Translation client automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # or other standard authentication methods.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # that your environment is otherwise authenticated for Google Cloud.

    client = translate.TranslationServiceClient()

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT") # Or specify your project ID directly
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set or project ID not provided.")

    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_text = response.translations[0].translated_text
    return translated_text

if __name__ == '__main__':
    # Example usage
    # Set environment variable GOOGLE_APPLICATION_CREDENTIALS pointing to your service account key file
    # and GOOGLE_CLOUD_PROJECT to your project ID.
    # For instance:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    french_appeal = "Je conteste cette décision. C'est une erreur."
    spanish_appeal = "Apelo esta decisión. Es un error."

    try:
        translated_french = translate_appeal_text(french_appeal, target_language="en")
        print(f"Original (French): '{french_appeal}'\nTranslated (English): '{translated_french}'\n")

        translated_spanish = translate_appeal_text(spanish_appeal, target_language="en")
        print(f"Original (Spanish): '{spanish_appeal}'\nTranslated (English): '{translated_spanish}'\n")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
