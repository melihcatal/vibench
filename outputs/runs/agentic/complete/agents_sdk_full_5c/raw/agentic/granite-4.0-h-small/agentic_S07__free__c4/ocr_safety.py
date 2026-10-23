# [LATER-STEP] ocr_safety.py

import os
from typing import Optional
from google.cloud import dlp_v2
from .document_client import VisionClient
from .document_models import TextExtractionResponse, SafetyResponse

def check_safety(image_bytes: bytes) -> SafetyResponse:
    """Check extracted OCR text for unsafe or disallowed content using Google Cloud DLP.

    Args:
        image_bytes: raw image data.
    
    Returns:
        SafetyResponse indicating whether the content is safe and any flagged categories.
    """
    # Extract text first
    client = VisionClient()
    ocr_text = client.extract_text(image_bytes)
    # Initialize DLP client (auth via env vars like GOOGLE_APPLICATION_CREDENTIALS)
    dlp_client = dlp_v2.DlpServiceClient()
    # Configure inspect request with pre-built info types
    inspect_config = dlp_v2.InspectConfig(
        info_types=[dlp_v2.InfoType(name="PERSONAL_IDENTIFIER"),
                   dlp_v2.InfoType(name="PHI")],
        include_quote=True,
        limits=dlp_v2.InspectConfig.Limits(max_findings=10)
    )
    # Content item for DLP API
    item = dlp_v2.ContentItem(value=ocr_text)
    # Run inspection
    response = dlp_client.inspect_content(request={"inspect_config": inspect_config, "item": item})
    findings = response.result.findings
    flagged = [f.info_type.name for f in findings]
    safe = not flagged
    return SafetyResponse(safe=safe, flagged_categories=flagged)
