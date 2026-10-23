from google.cloud import translate


class TranslationClient:
    def __init__(self, project_id: str = None):
        self.client = translate.TranslationServiceClient()
        self.project_id = project_id  # Google Cloud Translation requires project ID

    def get_client(self):
        return self.client

    def get_parent_path(self):
        return f"projects/{self.project_id}"
