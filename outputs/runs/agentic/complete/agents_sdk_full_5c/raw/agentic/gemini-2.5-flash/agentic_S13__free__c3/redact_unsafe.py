from google.cloud import dlp_v2
import os
from typing import List, Dict

def redact_unsafe(text: str, info_types: List[str] = None) -> Dict:
    """
    Flags or redacts unsafe spans from text using Google Cloud Data Loss Prevention (DLP) API.
    """
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")

    client = dlp_v2.DlpServiceClient()

    if info_types is None:
        # Default info types for common sensitive data, expand as needed for 'unsafe' context
        info_types = [
            "CREDIT_CARD_NUMBER", "EMAIL_ADDRESS", "PHONE_NUMBER", "US_SOCIAL_SECURITY_NUMBER",
            "IP_ADDRESS", "AGE", "GENERIC_PII"
        ]

    # The `inspect_config` defines what to look for, `redact_config` defines how to redact.
    # Here we are just inspecting, but the DLP API can also redact directly.
    # For redaction, you'd typically use `deidentify_content`.
    inspect_config = {
        "info_types": [{"name": info_type} for info_type in info_types],
        "include_quote": True,
    }

    item = {"value": text}

    # For redaction, uncomment and modify the below:
    # deidentify_config = {
    #     "info_type_transformations": {
    #         "transformations": [
    #             {
    #                 "info_types": [{"name": info_type} for info_type in info_types],
    #                 "primitive_transformation": {"redact_config": {}},
    #             }
    #         ]
    #     }
    # }
    # response = client.deidentify_content(
    #     request={
    #         "parent": f"projects/{project_id}/locations/global",
    #         "deidentify_config": deidentify_config,
    #         "inspect_config": inspect_config,
    #         "item": item,
    #     }
    # )
    # return {"redacted_text": response.item.value, "findings": response.overview_map}


    response = client.inspect_content(
        request={
            "parent": f"projects/{project_id}/locations/global",
            "inspect_config": inspect_config,
            "item": item,
        }
    )
    return {"original_text": text, "findings": response.result.findings}

if __name__ == '__main__':
    # Example usage:
    # Ensure GCP_PROJECT_ID is set and gcloud authentication is configured.
    # sensitive_text = "My email is test@example.com and my phone number is 123-456-7890."
    # result = redact_unsafe(sensitive_text)
    # print(result)
    pass
