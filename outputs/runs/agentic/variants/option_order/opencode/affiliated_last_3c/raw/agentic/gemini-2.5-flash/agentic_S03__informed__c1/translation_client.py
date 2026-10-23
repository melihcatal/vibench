from google.cloud import translate_v3beta1 as translate
import os


class GoogleTranslateClient:
    def __init__(self):
        self.client = translate.TranslationServiceClient()
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
        self.parent = f"projects/{self.project_id}"

    def get_client(self):
        return self.client

    def get_parent(self):
        return self.parent
