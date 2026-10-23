import os
from typing import Any, Dict

from google.cloud import documentai_v1 as documentai
from google.oauth2 import service_account

# Helper for creating and caching a Document AI client
class DocumentClient:
    _instance: Any = None
    _initialized: bool = False

    def __new__(cls) -> 'DocumentClient':
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _initialize(self) -> None:
        credentials = service_account.Credentials.from_service_account_file(
            os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
        self.client = documentai.DocumentProcessorServiceClient(credentials=credentials)
        self._initialized = True

    def _ensure_initialized(self) -> None:
        if not self._initialized:
            self._initialize()

    def process_document(self, name: str, raw_bytes: bytes, mime_type: str = 'application/pdf') -> Any:
        """Call the processor for OCR and layout extraction."""
        self._ensure_initialized()
        # Build the request payload for the processor
        request = documentai.ProcessRequest(
            name=name,
            raw_document=documentai.RawDocument(content=raw_bytes, mime_type=mime_type)
        )
        result = self.client.process_document(request=request)
        return result

# Singleton instance used throughout the same-scenario files
document_client = DocumentClient()