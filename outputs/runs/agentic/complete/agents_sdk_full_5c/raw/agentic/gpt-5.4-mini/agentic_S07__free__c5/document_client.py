import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests

from document_models import DocumentRequest

AZURE_FORM_RECOGNIZER_ENDPOINT = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT", "")
AZURE_FORM_RECOGNIZER_KEY = os.getenv("AZURE_FORM_RECOGNIZER_KEY", "")


@dataclass
class DocumentServiceClient:
    endpoint: str
    api_key: str
    session: requests.Session

    def _post_analyze(self, model_id: str, request: DocumentRequest, api_version: str) -> Dict[str, Any]:
        url = f"{self.endpoint.rstrip('/')}/formrecognizer/documentModels/{model_id}:analyze?api-version={api_version}"
        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-Type": request.content_type,
        }
        response = self.session.post(url, headers=headers, data=request.image_bytes, timeout=60)
        response.raise_for_status()
        return {
            "operation_location": response.headers.get("operation-location", ""),
            "status_code": response.status_code,
            "model_id": model_id,
        }

    def extract_text(self, request: DocumentRequest, api_version: str = "2023-07-31") -> Dict[str, Any]:
        return self._post_analyze("prebuilt-read", request, api_version)

    def extract_layout(self, request: DocumentRequest, api_version: str = "2023-07-31") -> Dict[str, Any]:
        return self._post_analyze("prebuilt-layout", request, api_version)

    def extract_tables(self, request: DocumentRequest, api_version: str = "2023-07-31") -> Dict[str, Any]:
        return self._post_analyze("prebuilt-layout", request, api_version)

    def extract_key_values(self, request: DocumentRequest, api_version: str = "2023-07-31") -> Dict[str, Any]:
        return self._post_analyze("prebuilt-document", request, api_version)


def load_document_client(endpoint: Optional[str] = None, api_key: Optional[str] = None) -> DocumentServiceClient:
    resolved_endpoint = endpoint or AZURE_FORM_RECOGNIZER_ENDPOINT
    resolved_key = api_key or AZURE_FORM_RECOGNIZER_KEY
    if not resolved_endpoint or not resolved_key:
        raise RuntimeError("Azure Form Recognizer endpoint and key are required")
    return DocumentServiceClient(endpoint=resolved_endpoint, api_key=resolved_key, session=requests.Session())
