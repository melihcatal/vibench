import os
from typing import Dict, Any, List
import requests
from document_models import FieldExtractionResponse


def extract_fields(text: str, field_schema: Dict[str, str]) -> FieldExtractionResponse:
    """
    Extract structured fields from OCR-normalized document text using Google Cloud Document AI.
    """
    processor_id = os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_ID")
    location = os.getenv("GOOGLE_DOCUMENT_AI_LOCATION", "us")
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    
    if not processor_id or not project_id:
        raise ValueError("GOOGLE_DOCUMENT_AI_PROCESSOR_ID or GOOGLE_CLOUD_PROJECT_ID not set")
    
    # Google Document AI-specific request
    endpoint = f"https://{location}-documentai.googleapis.com/v1/projects/{project_id}/locations/{location}/processors/{processor_id}:process"
    
    request_payload = {
        "rawDocument": {
            "content": text,
            "mimeType": "text/plain"
        }
    }
    
    response = requests.post(
        endpoint,
        json=request_payload,
        headers={
            "Authorization": f"Bearer {_get_google_access_token()}",
            "Content-Type": "application/json"
        }
    )
    response.raise_for_status()
    
    result = response.json()
    fields = {}
    for entity in result.get("document", {}).get("entities", []):
        field_name = entity.get("type", "")
        if field_name in field_schema:
            fields[field_schema[field_name]] = entity.get("mentionText", "")
    
    return FieldExtractionResponse(
        fields=fields,
        provider="google_document_ai",
        raw_response=result
    )


def _get_google_access_token() -> str:
    """Retrieve Google Cloud access token for Document AI."""
    from google.auth import jwt
    from google.auth.transport import requests
    
    credentials, _ = jwt.Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        audience="https://oauth2.googleapis.com/token"
    )
    request = requests.Request()
    credentials.refresh(request)
    return credentials.token