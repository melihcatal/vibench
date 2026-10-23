from google.cloud import dlp_v2

def redact_unsafe_content(project_id: str, text_content: str) -> str:
    """Redacts unsafe spans from the text using Google Cloud DLP.

    Args:
        project_id: The Google Cloud project ID.
        text_content: The text content to redact.

    Returns:
        The text with unsafe spans redacted.
    """
    dlp_client = dlp_v2.DlpServiceClient()

    # Define the info types to look for. These are examples of "unsafe" or sensitive data.
    info_types = [
        {"name": "EMAIL_ADDRESS"},
        {"name": "PHONE_NUMBER"},
        {"name": "CREDIT_CARD_NUMBER"},
        {"name": "US_SOCIAL_SECURITY_NUMBER"},
        {"name": "IP_ADDRESS"},
        {"name": "PERSON_NAME"},
    ]

    # Configure the redaction method (replace with info type name)
    deidentify_config = {
        "info_type_transformations": {
            "transformations": [
                {
                    "info_types": info_types,
                    "primitive_transformation": {
                        "replace_with_info_type_config": {}
                    },
                }
            ]
        }
    }

    # Configure the inspection to specify the info types to be detected.
    inspect_config = {"info_types": info_types}

    # Create a content item
    item = {"value": text_content}

    # Construct the parent resource path
    parent = f"projects/{project_id}/locations/global"

    # Call the API
    response = dlp_client.deidentify_content(
        request={
            "parent": parent,
            "deidentify_config": deidentify_config,
            "inspect_config": inspect_config,
            "item": item,
        }
    )

    return response.item.value

