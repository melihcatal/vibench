import base64
import json
import os
import urllib.request
from typing import Any, Dict, Optional


GOOGLE_DOCUMENT_AI_ENDPOINT = "https://documentai.googleapis.com/v1/projects/{project_id}/locations/{location}/processors/{processor_id}:process"


class GoogleDocumentAITableExtractor:
    def __init__(self, project_id: Optional[str] = None, location: Optional[str] = None, processor_id: Optional[str] = None, api_key: Optional[str] = None) -> None:
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        self.location = location or os.environ.get("GOOGLE_DOCUMENT_AI_LOCATION", "us")
        self.processor_id = processor_id or os.environ.get("GOOGLE_DOCUMENT_AI_PROCESSOR_ID")
        self.api_key = api_key or os.environ.get("GOOGLE_DOCUMENT_AI_API_KEY")

    def extract_tables(self, document_bytes: bytes) -> Dict[str, Any]:
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT is required")
        if not self.processor_id:
            raise ValueError("GOOGLE_DOCUMENT_AI_PROCESSOR_ID is required")

        url = GOOGLE_DOCUMENT_AI_ENDPOINT.format(
            project_id=self.project_id,
            location=self.location,
            processor_id=self.processor_id,
        )
        if self.api_key:
            url = f"{url}?key={self.api_key}"

        payload = {
            "rawDocument": {
                "content": base64.b64encode(document_bytes).decode("ascii"),
                "mimeType": "application/pdf",
            }
        }
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))

        document = result.get("document", {})
        tables = document.get("pages", [])
        extracted_tables = []
        for page in tables:
            for table in page.get("tables", []):
                extracted_tables.append(table)

        return {"provider": "google-document-ai", "tables": extracted_tables, "raw": result}


def extract_tables(document_bytes: bytes, project_id: Optional[str] = None, location: Optional[str] = None, processor_id: Optional[str] = None, api_key: Optional[str] = None) -> Dict[str, Any]:
    return GoogleDocumentAITableExtractor(project_id=project_id, location=location, processor_id=processor_id, api_key=api_key).extract_tables(document_bytes=document_bytes)
