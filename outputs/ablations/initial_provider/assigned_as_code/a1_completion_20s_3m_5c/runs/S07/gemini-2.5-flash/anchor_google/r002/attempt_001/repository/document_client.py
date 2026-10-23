import os
from google.cloud import documentai_v1 as documentai
from google.cloud import translate_v3 as translate
from google.cloud import aiplatform

class DocumentClient:
    def __init__(self, project_id: str, location: str):
        self.project_id = project_id
        self.location = location
        self._documentai_client = None
        self._translate_client = None
        self._aiplatform_client = None

    @property
    def documentai_client(self):
        if self._documentai_client is None:
            self._documentai_client = documentai.DocumentProcessorServiceClient(
                client_options={"api_endpoint": f"{self.location}-documentai.googleapis.com"}
            )
        return self._documentai_client

    @property
    def translate_client(self):
        if self._translate_client is None:
            self._translate_client = translate.TranslationServiceClient()
        return self._translate_client

    @property
    def aiplatform_client(self):
        if self._aiplatform_client is None:
            aiplatform.init(project=self.project_id, location=self.location)
            self._aiplatform_client = aiplatform
        return self._aiplatform_client

    def get_document_processor_path(self, processor_id: str):
        return self.documentai_client.processor_path(
            self.project_id, self.location, processor_id
        )
