import os
from google.cloud import dlp_v2


def redact_unsafe_content(
    text_content: str, project_id: str, info_types: list = None
) -> str:
    """Flags or redacts unsafe spans from text using Google Cloud Data Loss Prevention (DLP) API.

    Args:
        text_content: The text to redact.
        project_id: The Google Cloud project ID.
        info_types: A list of info types to detect and redact. Defaults to common PII.

    Returns:
        The redacted text.
    """
    if info_types is None:
        info_types = [
            "CREDIT_CARD_NUMBER",
            "EMAIL_ADDRESS",
            "PHONE_NUMBER",
            "US_SOCIAL_SECURITY_NUMBER",
            "IP_ADDRESS",
        ]

    client = dlp_v2.DlpServiceClient()
    # Construct the `inspect_config` to specify the `info_types` to detect.
    inspect_config = {"info_types": [{"name": info_type} for info_type in info_types]}

    # Construct the `redact_config` to replace detected sensitive data with a fixed string.
    redact_config = {
        "info_type_transformations": [
            {
                "info_types": [{"name": info_type} for info_type in info_types],
                "primitive_transformation": {
                    "character_masking_config": {"masking_character": "#"}
                },
            }
        ]
    }

    # Construct the `item` to be inspected.
    item = {"value": text_content}

    parent = f"projects/{project_id}/locations/global"

    response = client.deidentify_content(
        request={
            "parent": parent,
            "deidentify_config": {
                "info_type_transformations": redact_config["info_type_transformations"]
            },
            "inspect_config": inspect_config,
            "item": item,
        }
    )

    return response.item.value


if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    if project_id == "your-gcp-project-id":
        print(
            "Please set the GOOGLE_CLOUD_PROJECT environment variable or replace 'your-gcp-project-id' with your actual project ID."
        )
    else:
        text_with_pii = (
            "My email is test@example.com and my phone number is 123-456-7890."
        )
        redacted_text = redact_unsafe_content(text_with_pii, project_id)
        print(f"Original text: '{text_with_pii}'")
        print(f"Redacted text: '{redacted_text}'")

        text_with_ssn = "My SSN is 000-11-2222."
        redacted_ssn = redact_unsafe_content(
            text_with_ssn, project_id, info_types=["US_SOCIAL_SECURITY_NUMBER"]
        )
        print(f"Original text: '{text_with_ssn}'")
        print(f"Redacted text: '{redacted_ssn}'")
