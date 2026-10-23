import os
from google.cloud import translate_v3 as translate

class GeneralTranslationClient:
    def __init__(self):
        self.client = translate.TranslationServiceClient()
        self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
        self.parent = f"projects/{self.project_id}/locations/global"

    def get_client(self) -> translate.TranslationServiceClient:
        return self.client

    def get_parent_path(self) -> str:
        return self.parent
