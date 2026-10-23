# [LATER-STEP] ocr_safety.py
"""Check extracted OCR text for unsafe or sensitive content"""

import os
from typing import Dict, Any
from google.cloud import dlp_v2 as dlp


# Load configuration (API key / credentials) from helper if needed
def get_dlp_client() -> dlp.DlpServiceClient:
    """Create a Google Cloud DLP client"""
    return dlp.DlpServiceClient()


def scan_text_for_sensitive(text: str) -> Dict[str, Any]:
    """Scan text for PII, profanity, etc., using Google DLP"""
    client = get_dlp_client()
    # Define inspection config (example: find phone numbers, emails, IDs)
    inspect_config = {
        "info_types": [
            {"name": "PHONE_NUMBER"},
            {"name": "EMAIL_ADDRESS"},
            {"name": "ID_NUMBER"},
        ]
    }
    # The content item to inspect
    content_item = {"type_": "TEXT", "value": text}
    # Run inspection
    response = client.inspect_content(
        request={"inspect_config": inspect_config, "item": content_item}
    )
    findings = response.result.findings
    result = {
        "total_findings": len(findings),
        "items": [
            {
                "info_type": f.name,
                "value": f.quote,
                "confidence": f.info_type_confidence,
            }
            for f in findings
        ],
    }
    return result


if __name__ == "__main__":
    import json, sys

    if len(sys.argv) != 2:
        print("Usage: python ocr_safety.py <ocr-json>")
        sys.exit(1)
    with open(sys.argv[1], "r") as f:
        ocr_json = json.load(f)
    text = " ".join(b["Text"] for b in ocr_json.get("Blocks", []))
    print(json.dumps(scan_text_for_sensitive(text), indent=2))
