from __future__ import annotations

import base64
import os
from typing import Any, Dict, Optional

import requests


GOOGLE_DOCAI_API_ROOT = "https://us-documentai.googleapis.com/v1"


class GoogleDocumentAIClient:
    def __init__(
        self,
        project_id: Optional[str] = None,
        location: Optional[str] = None,
        processor_id: Optional[str] = None,
        access_token: Optional[str] = None,
        timeout: int = 60,
    ) -> None:
        self.project_id = project_id or os.environ["GOOGLE_CLOUD_PROJECT"]
        self.location = location or os.environ.get("GOOGLE_DOCAI_LOCATION", "us")
        self.processor_id = processor_id or os.environ["GOOGLE_DOCAI_PROCESSOR_ID"]
        self.access_token = access_token or os.environ["GOOGLE_DOCAI_ACCESS_TOKEN"]
        self.timeout = timeout

    @property
    def processor_name(self) -> str:
        return f"projects/{self.project_id}/locations/{self.location}/processors/{self.processor_id}"

    def process_document(
        self, content: bytes, mime_type: str, field_mask: Optional[str] = None
    ) -> Dict[str, Any]:
        url = f"{GOOGLE_DOCAI_API_ROOT}/{self.processor_name}:process"
        payload: Dict[str, Any] = {
            "rawDocument": {
                "content": base64.b64encode(content).decode("utf-8"),
                "mimeType": mime_type,
            }
        }
        if field_mask:
            payload["fieldMask"] = field_mask
        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()


def get_google_document_ai_client(
    processor_id: Optional[str] = None,
) -> GoogleDocumentAIClient:
    return GoogleDocumentAIClient(processor_id=processor_id)
