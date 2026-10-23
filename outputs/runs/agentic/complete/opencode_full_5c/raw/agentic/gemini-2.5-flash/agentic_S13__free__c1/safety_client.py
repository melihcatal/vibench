import os
from google.cloud import (
    aiplatform,
    dlp_v2,
    translate_v3,
    texttospeech_v1,
    secretmanager,
)
from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from msrest.authentication import CognitiveServicesCredentials


class GoogleSafetyClient:
    def __init__(self, project_id: str, location: str):
        self.project_id = project_id
        self.location = location
        aiplatform.init(project=project_id, location=location)
        self.vertex_ai_client = aiplatform.gapic.PredictionServiceClient()
        self.dlp_client = dlp_v2.DlpServiceClient()
        self.translate_client = translate_v3.TranslationServiceClient()
        self.text_to_speech_client = texttospeech_v1.TextToSpeechClient()
        self.secret_manager_client = secretmanager.SecretManagerServiceClient()

    def get_vertex_ai_model(self, model_id: str):
        return self.vertex_ai_client.endpoint_path(
            self.project_id, self.location, model_id
        )

    def get_dlp_parent(self):
        return f"projects/{self.project_id}"

    def get_secret_version(self, secret_id: str, version_id: str = "latest"):
        name = self.secret_manager_client.secret_version_path(
            self.project_id, secret_id, version_id
        )
        response = self.secret_manager_client.access_secret_version(
            request={"name": name}
        )
        return response.payload.data.decode("UTF-8")


class AzureSafetyClient:
    def __init__(self, subscription_key: str, endpoint: str):
        self.content_moderator_client = ContentModeratorClient(
            CognitiveServicesCredentials(subscription_key), endpoint
        )
