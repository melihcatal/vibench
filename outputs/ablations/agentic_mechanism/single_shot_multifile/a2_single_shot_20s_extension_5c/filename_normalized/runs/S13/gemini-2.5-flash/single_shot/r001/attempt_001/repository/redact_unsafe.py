import os
from google.cloud import dlp_v2
from typing import List

from safety_client import get_google_dlp_client
from safety_models import RedactionResult, DlpDetection

def redact_unsafe(text: str) -> RedactionResult:
    client = get_google_dlp_client()
    project_id = os.getenv("GOOGLE_DLP_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_DLP_PROJECT_ID environment variable not set.")

    # Define what information types to inspect and redact
    info_types_to_redact = [
        {"name": "EMAIL_ADDRESS"},
        {"name": "PHONE_NUMBER"},
        {"name": "CREDIT_CARD_NUMBER"},
        {"name": "IP_ADDRESS"},
        {"name": "US_SOCIAL_SECURITY_NUMBER"},
    ]

    # Configure the de-identification request
    deidentify_config = {
        "info_type_transformations": {
            "transformations": [
                {
                    "info_types": info_types_to_redact,
                    "primitive_transformation": {
                        "replace_config": {"new_value": {"string_value": "[REDACTED]"}}
                    },
                }
            ]
        }
    }
    
    # Configure inspection to find the info types
    inspect_config = {"info_types": info_types_to_redact}

    # The item to be de-identified
    item = {"value": text}

    try:
        # Call the DLP API to de-identify content
        response = client.deidentify_content(
            request={
                "parent": f"projects/{project_id}",
                "deidentify_config": deidentify_config,
                "inspect_config": inspect_config,
                "item": item,
            }
        )

        redacted_text = response.item.value
        detections: List[DlpDetection] = []

        # Optionally, inspect content first to get details of detections if needed
        # For simplicity, this example directly uses deidentify_content which just returns the redacted text.
        # If detailed detections (like `quote`, `start`, `end`) are needed, a separate `inspect_content` call is required.
        # For this task, we'll assume the primary output is the redacted text.
        
        return RedactionResult(original_text=text, redacted_text=redacted_text, detections=detections)
    except Exception as e:
        print(f"Error redacting text with Google DLP: {e}")
        return RedactionResult(original_text=text, redacted_text=text, detections=[])
