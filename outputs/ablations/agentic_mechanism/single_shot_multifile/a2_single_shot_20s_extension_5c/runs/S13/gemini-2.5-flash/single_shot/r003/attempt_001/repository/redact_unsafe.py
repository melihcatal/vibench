import os
from typing import List, Dict, Any
from google.cloud import dlp_v2

from safety_client import get_google_dlp_client
from safety_models import RedactionResult

def redact_unsafe(text_content: str, info_types: List[str] = None) -> RedactionResult:
    client = get_google_dlp_client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    # Default info types for common sensitive data, can be extended or customized
    if info_types is None:
        info_types = [
            "PERSON_NAME",
            "EMAIL_ADDRESS",
            "PHONE_NUMBER",
            "CREDIT_CARD_NUMBER",
            "IP_ADDRESS",
            "DATE_OF_BIRTH",
            "LOCATION",
            "GENERIC_PII"
        ]

    item = {"value": text_content}

    inspect_config = {
        "info_types": [{"name": itype} for itype in info_types],
        "include_quote": True,
    }

    # Use a replace config to redact findings with a placeholder like "[REDACTED]"
    # or use a transform_action for more specific redaction (e.g., using info_type name)
    deidentify_config = {
        "info_type_transformations": {
            "transformations": [
                {
                    "info_types": [{"name": itype} for itype in info_types],
                    "primitive_transformation": {
                        "replace_config": {
                            "new_value": {
                                "string_value": "[REDACTED]"
                            }
                        }
                    }
                }
            ]
        }
    }

    # The parent for the resource. (e.g. `projects/{project_id}`)
    parent = f"projects/{project_id}"

    response = client.deidentify_content(
        request={
            "parent": parent,
            "deidentify_config": deidentify_config,
            "inspect_config": inspect_config,
            "item": item,
        }
    )

    detected_types = []
    if response.overview and response.overview.transformed_bytes: # Check if transformations occurred
        # DLP doesn't directly return the *types* that were transformed in the deidentify_content response itself,
        # but rather the byte counts. A separate inspect_content call would be needed to get detailed findings.
        # For simplicity, if redaction happens, we can assume one of the requested info_types was found.
        # A more robust solution would involve first inspecting, then de-identifying specific findings.
        # Here, we'll indicate if any redaction occurred by comparing original and redacted text.
        if response.item.value != text_content:
             detected_types = ["Potentially Sensitive Info"]
    
    return RedactionResult(
        original_text=text_content,
        redacted_text=response.item.value,
        detected_info_types=detected_types # Simplified detection indication
    )
