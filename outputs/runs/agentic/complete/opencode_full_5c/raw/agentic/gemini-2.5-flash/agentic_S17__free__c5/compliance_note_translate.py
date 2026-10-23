import os
from google.cloud import translate_v3
from security_models import TranslationRequest, TranslationResponse


def translate_compliance_note(request: TranslationRequest) -> TranslationResponse:
    """
    Translates encryption or compliance notes for reviewers using Google Cloud Translation.
    """
    translation_client = translate_v3.TranslationServiceClient()

    # The `parent` argument requires a project number or project ID.
    parent = f"projects/{request.project_id}/locations/global"

    response = translation_client.translate_text(
        request={
            "parent": parent,
            "contents": [request.text_content],
            "target_language_code": request.target_language_code,
            "source_language_code": request.source_language_code,
        }
    )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text

    return TranslationResponse(translated_text=translated_text)


if __name__ == "__main__":
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")

    if PROJECT_ID == "your-gcp-project-id":
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable.")
    else:
        sample_note_en = "Encryption policies for customer data are in compliance with GDPR regulations."
        sample_note_fr = "Les politiques de chiffrement des données clients sont conformes aux réglementations GDPR."

        # Translate from English to Spanish
        translate_to_es_request = TranslationRequest(
            text_content=sample_note_en,
            target_language_code="es",
            project_id=PROJECT_ID,
            source_language_code="en",
        )
        print(f"Translating '{sample_note_en}' from English to Spanish...")
        response_es = translate_compliance_note(translate_to_es_request)
        print(f"Translated to Spanish: {response_es.translated_text}")

        # Translate from French to English
        translate_to_en_request = TranslationRequest(
            text_content=sample_note_fr,
            target_language_code="en",
            project_id=PROJECT_ID,
            source_language_code="fr",
        )
        print(f"Translating '{sample_note_fr}' from French to English...")
        response_en = translate_compliance_note(translate_to_en_request)
        print(f"Translated to English: {response_en.translated_text}")
