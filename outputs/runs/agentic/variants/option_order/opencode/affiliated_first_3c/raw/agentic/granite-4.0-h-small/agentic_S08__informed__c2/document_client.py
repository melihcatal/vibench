# document_client.py
# [HELPER]
# Local configuration and client helper utilities for Structured Document Extraction.

import os
from typing import Dict, Any

# Configure AWS credentials for Textract via environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Configure Google Document AI credentials via environment variables
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Placeholder for Document AI endpoint - adjust as needed
DOCUMENT_AI_ENDPOINT = "https://documentai.googleapis.com/v1/projects/YOUR_PROJECT/locations/us/processors/YOUR_INVOICE_PROCESSOR:process"


# Simple request wrapper that injects auth information where needed
def build_request(payload: Dict[str, Any], service: str) -> Dict[str, Any]:
    """Inject authentication information into a request payload.

    Args:
        payload: Base request data.
        service: Service name to determine auth method (e.g., 'google', 'aws').

    Returns:
        Payload with added credentials.
    """
    if service == "google":
        payload["headers"] = {
            "Authorization": f"Bearer {GOOGLE_APPLICATION_CREDENTIALS}"
        }
    elif service == "aws":
        payload["aws"] = {
            "access_key": AWS_ACCESS_KEY_ID,
            "secret_key": AWS_SECRET_ACCESS_KEY,
        }
    return payload


# Example generic HTTP request for providers that require REST calls
def generic_request(
    url: str, method: str = "POST", payload: Dict[str, Any] = None, service: str = None
):
    """Perform a generic HTTP request and return JSON response.

    This is a stub - replace with proper HTTP client (requests, httpx, etc.) in
    production.
    """
    # Stub response for illustration
    return {"status": "success", "service": service, "data": payload}


# Example usage (remove in production)
if __name__ == "__main__":
    # Build a request for Google Document AI
    req = build_request({"document_path": "invoice.pdf"}, service="google")
    # Call generic_request stub
    resp = generic_request(
        url=DOCUMENT_AI_ENDPOINT, method="POST", payload=req, service="google"
    )
    print(resp)
