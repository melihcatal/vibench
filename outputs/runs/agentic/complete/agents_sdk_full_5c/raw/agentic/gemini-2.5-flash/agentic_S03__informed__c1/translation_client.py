from google.cloud import translate_v3 as translate
import os

class TranslationClient:
    def __init__(self, project_id: str = None):
        if project_id is None:
            self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
            if self.project_id is None:
                raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
        else:
            self.project_id = project_id
        self._client = translate.TranslationServiceClient()
        self._parent = f"projects/{self.project_id}/locations/global"

    def get_client(self) -> translate.TranslationServiceClient:
        return self._client

    def get_parent_path(self) -> str:
        return self._parent

    def get_project_id(self) -> str:
        return self.project_id
