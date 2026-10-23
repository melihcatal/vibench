import os
from typing import List, Dict, Any
from security_client import SecurityClient
from security_models import PayloadSafetyRequest, PayloadSafetyResponse


def check_payload_safety(request: PayloadSafetyRequest) -> PayloadSafetyResponse:
    client = SecurityClient()
    has_unsafe_content, findings = client.check_payload_safety_with_dlp(
        project_id=request.project_id,
        content=request.content,
        location_id=request.location_id,
    )
    return PayloadSafetyResponse(
        has_unsafe_content=has_unsafe_content, findings=findings
    )
