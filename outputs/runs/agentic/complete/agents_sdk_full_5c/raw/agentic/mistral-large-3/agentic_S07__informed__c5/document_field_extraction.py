import os
from typing import Dict, Any, List
from google.cloud import documentai_v1 as documentai


class DocumentFieldExtractor:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        self.location = "us"
        self.processor_id = os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_ID")
        self.client = documentai.DocumentProcessorServiceClient()
        self.processor_name = self.client.processor_path(
            self.project_id, self.location, self.processor_id
        )

    def extract_fields(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, "rb") as f:
            document = {"content": f.read(), "mime_type": "application/pdf"}
        request = {"name": self.processor_name, "raw_document": document}
        result = self.client.process_document(request=request)
        return self._parse_result(result.document)

    def _parse_result(self, document: documentai.Document) -> Dict[str, Any]:
        fields = {}
        for entity in document.entities:
            fields[entity.type_] = entity.mention_text
        return fields