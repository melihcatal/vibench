import os
from google.cloud import translate_v3 as translate
from model_models import TranslationRequest, TranslationResponse


class GoogleCloudTranslationClient:
    def __init__(self):
        self.client = translate.TranslationServiceClient()
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        if not self.project_id:
            raise ValueError(
                "GOOGLE_CLOUD_PROJECT_ID environment variable must be set."
            )

    def translate_text(self, request: TranslationRequest) -> TranslationResponse:
        parent = f"projects/{self.project_id}/locations/global"

        response = self.client.translate_text(
            request={
                "parent": parent,
                "contents": [request.text],
                "target_language_code": request.target_language_code,
                "source_language_code": request.source_language_code
                if request.source_language_code
                else None,
            }
        )

        translated_text = (
            response.translations[0].translated_text if response.translations else ""
        )
        return TranslationResponse(translated_text=translated_text)


def translate_model_output(request: TranslationRequest) -> TranslationResponse:
    client = GoogleCloudTranslationClient()
    return client.translate_text(request)
