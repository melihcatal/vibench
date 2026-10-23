import os
from google.cloud import documentai_v1beta3 as documentai
from google.api_core.client_options import ClientOptions
from dotenv import load_dotenv

load_dotenv()


class DocumentClient:
    def __init__(self):
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        location = os.getenv(
            "GOOGLE_CLOUD_LOCATION", "us"
        )  # Default to 'us' if not set
        self.project_id = project_id
        self.location = location

        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

        # Document AI client for document processing
        docai_client_options = ClientOptions(
            api_endpoint=f"{self.location}-documentai.googleapis.com"
        )
        self.documentai_client = documentai.DocumentProcessorServiceClient(
            client_options=docai_client_options
        )

    def get_documentai_processor_path(self, processor_id: str) -> str:
        return self.documentai_client.processor_path(
            self.project_id, self.location, processor_id
        )
