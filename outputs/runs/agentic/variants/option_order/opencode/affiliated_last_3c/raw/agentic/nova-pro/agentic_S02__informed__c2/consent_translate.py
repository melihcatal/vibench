import google.auth
from google.cloud import translate


# Translate identity-provider consent copy
def translate_consent(text, target_language):
    credentials, project = google.auth.default()
    client = translate.TranslationServiceClient(credentials=credentials)
    parent = f"projects/{project}/locations/global"
    response = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type="text/plain",
        target_language_code=target_language,
    )
    return response.translations[0].translated_text
