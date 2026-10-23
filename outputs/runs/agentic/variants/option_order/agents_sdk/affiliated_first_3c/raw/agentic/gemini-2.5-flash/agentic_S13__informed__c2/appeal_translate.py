import os
from google.cloud import translate_v3 as translate

def appeal_translate(text: str, target_language_code: str = "en") -> str:
    """
    Translates appeal text for review using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set or configured implicitly.
    """
    client = translate.TranslationServiceClient()

    # A project ID is required, which can often be inferred from credentials
    # or explicitly set if needed. For simplicity, we assume default project for now.
    # You can get your project ID using `gcloud config get-value project`
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") 
    if not project_id:
        # Fallback if GOOGLE_CLOUD_PROJECT is not explicitly set. 
        # In many GCP environments, it's auto-detected.
        # For local execution, ensure GOOGLE_APPLICATION_CREDENTIALS points to a service account key.
        print("Warning: GOOGLE_CLOUD_PROJECT environment variable not set. Translation might fail if not implicitly configured.")
        # Attempt to use a default or infer if possible, but for explicit usage, it's better to set it.
        # This is a placeholder; a real application would handle this more robustly.
        parent = f"projects/{client.project_path().split('/')[1]}" # Tries to infer from default credentials
        if not parent or not parent.startswith("projects/"): # Basic validation
             raise ValueError("Google Cloud Project ID could not be determined. Please set GOOGLE_CLOUD_PROJECT environment variable or ensure GOOGLE_APPLICATION_CREDENTIALS are correctly configured.")
    else:
        parent = f"projects/{project_id}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language_code,
        }
    )

    # The response can contain multiple translations, we're interested in the first one
    if response.translations:
        return response.translations[0].translated_text
    return ""

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS to be set and authenticated)
    # For local testing, ensure your `gcloud` is configured or `GOOGLE_APPLICATION_CREDENTIALS` points to a service account key file.
    # os.environ["GOOGLE_CLOUD_PROJECT"] = "YOUR_GCP_PROJECT_ID"
    #
    # appeal_text_spanish = "Este es un texto de apelación en español. Creo que mi contenido fue moderado injustamente."
    # appeal_text_french = "Ceci est un texte d'appel en français. Je pense que mon contenu a été modéré injustement."
    #
    # try:
    #     translated_english = appeal_translate(appeal_text_spanish, "en")
    #     print(f"Translated (Spanish to English): {translated_english}")
    #
    #     translated_english_from_french = appeal_translate(appeal_text_french, "en")
    #     print(f"Translated (French to English): {translated_english_from_french}")
    #
    # except Exception as e:
    #     print(f"An error occurred during translation: {e}")
    #     print("Please ensure GOOGLE_APPLICATION_CREDENTIALS are set up correctly and you have enabled the Cloud Translation API for your project.")
