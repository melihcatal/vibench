from google.cloud import translate_v3 as translate
import os

class TranslationClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TranslationClient, cls).__new__(cls)
            cls._instance.client = translate.TranslationServiceClient()
            cls._instance.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
            if not cls._instance.project_id:
                raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
            cls._instance.parent = f"projects/{cls._instance.project_id}"
        return cls._instance

    def get_client(self):
        return self.client

    def get_parent_path(self):
        return self.parent
