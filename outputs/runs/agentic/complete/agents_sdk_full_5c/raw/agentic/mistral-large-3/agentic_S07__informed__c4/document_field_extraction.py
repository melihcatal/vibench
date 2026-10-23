from typing import Dict, Any, Optional
from google.cloud import documentai_v1 as documentai
import os


class DocumentFieldExtractor:
    def __init__(self):
        self.client = documentai.DocumentProcessorServiceClient()
        self.processor_name = os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_NAME")
        if not self.processor_name:
            raise ValueError(
                "Google Document AI processor name must be set as GOOGLE_DOCUMENT_AI_PROCESSOR_NAME."
            )

    def extract_fields(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, "rb") as file:
            file_content = file.read()

        request = documentai.ProcessRequest(
            name=self.processor_name, raw_document=documentai.RawDocument(content=file_content, mime_type="application/pdf")
        )
        result = self.client.process_document(request=request)
        return documentai.Document.to_dict(result.document)