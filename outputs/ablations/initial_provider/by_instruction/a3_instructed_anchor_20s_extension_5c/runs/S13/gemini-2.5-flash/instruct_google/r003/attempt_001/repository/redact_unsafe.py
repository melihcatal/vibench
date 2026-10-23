import os
from typing import List, Dict, Any
from google.cloud import dlp_v2
from safety_client import SafetyClient

def redact_unsafe(text: str, info_types: List[str] = None) -> Dict[str, Any]:
    """
    Flags or redacts unsafe spans from text using Google Cloud DLP API.
    By default, redacts common PII. Custom info_types can be provided.
    """
    if info_types is None:
        info_types = [
            "PHONE_NUMBER", "EMAIL_ADDRESS", "CREDIT_CARD_NUMBER",
            "IP_ADDRESS", "US_SOCIAL_SECURITY_NUMBER", "PASSPORT",
            "PERSON_NAME", "LOCATION", "DATE_OF_BIRTH"
        ]

    safety_client = SafetyClient()
    dlp_client = safety_client.get_dlp_client()
    project_id = safety_client.project_id

    # Construct the `inspect_config` to specify the info_types to look for
    inspect_config = {"info_types": [{"name": info_type} for info_type in info_types]}

    # Construct the `redact_config` to replace identified sensitive data with a placeholder
    redact_config = {"info_type_transformations": []}
    for info_type in info_types:
        redact_config["info_type_transformations"].append({
            "info_types": [{"name": info_type}],
            "primitive_transformation": {"character_masking_config": {"masking_character": "*"}}
        })

    # Construct the `deidentify_config`
    deidentify_config = {"info_type_transformations": redact_config["info_type_transformations"]}

    # Construct the `item` to be de-identified
    item = {"value": text}

    # Call the DLP API to de-identify the content
    response = dlp_client.deidentify_content(
        request={
            "parent": f"projects/{project_id}/locations/{safety_client.location}",
            "deidentify_config": deidentify_config,
            "inspect_config": inspect_config,
            "item": item,
        }
    )

    return {"redacted_text": response.item.value}
