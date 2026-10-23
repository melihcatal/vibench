import os
from typing import List

from google.cloud import dlp_v2

from safety_client import get_gcp_project_id


def redact_unsafe(text: str, info_types: List[str] = None) -> str:
    """
    Redacts unsafe content (profanity by default) from text using Google Cloud DLP.

    Args:
        text: The text to redact.
        info_types: A list of infoType detectors to use, e.g., ["PROFANITY"].

    Returns:
        The text with identified spans redacted.
    """
    project_id = get_gcp_project_id()
    if not project_id:
        raise ValueError("Google Cloud Project ID is not set.")

    if info_types is None:
        info_types = ["PROFANITY"]

    dlp_client = dlp_v2.DlpServiceClient()

    parent = f"projects/{project_id}"

    inspect_config = {
        "info_types": [{"name": info_type} for info_type in info_types],
        "include_quote": True,
    }

    deidentify_config = {
        "info_type_transformations": {
            "transformations": [
                {
                    "primitive_transformation": {
                        "replace_with_info_type_config": {}
                    }
                }
            ]
        }
    }

    item = {"value": text}

    try:
        response = dlp_client.deidentify_content(
            request={
                "parent": parent,
                "deidentify_config": deidentify_config,
                "inspect_config": inspect_config,
                "item": item,
            }
        )
        return response.item.value
    except Exception as e:
        print(f"An error occurred with Google Cloud DLP: {e}")
        return text
