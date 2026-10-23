import os
from google.cloud import dlp_v2

def redact_unsafe_spans(text: str, project_id: str) -> str:
    """Redacts unsafe/sensitive spans from the given text using Google Cloud DLP.

    Args:
        text: The input text to redact.
        project_id: The Google Cloud project ID.

    Returns:
        The text with unsafe spans redacted.
    """
    if not project_id:
        raise ValueError("Google Cloud project ID must be provided.")

    dlp_client = dlp_v2.DlpServiceClient()

    # Define the info types to be redacted.
    # For a general definition of "unsafe", we'll consider common sensitive data.
    # This can be customized based on specific "unsafe" criteria.
    info_types = [
        {"name": "EMAIL_ADDRESS"},
        {"name": "PHONE_NUMBER"},
        {"name": "CREDIT_CARD_NUMBER"},
        {"name": "IP_ADDRESS"},
        {"name": "US_SOCIAL_SECURITY_NUMBER"},
        {"name": "DATE_OF_BIRTH"},
        {"name": "PERSON_NAME"},
    ]

    # The type of the content to inspect.
    item = {"value": text}

    # The action to perform on the sensitive data. Here, we redact it.
    # You can choose different redaction configurations.
    redact_config = {"info_type_name_transformations": {"transformations": [{"info_types": info_types, "redaction_config": {"info_type_config": {}}}]}}

    # Construct the deidentify config.
    deidentify_config = {
        "info_type_transformations": {
            "transformations": [
                {
                    "info_types": info_types,
                    "primitive_transformation": {"replace_config": {"new_value": {"character_mask_config": {"masking_character": "#", "number_to_mask": 0}}}}
                }
            ]
        }
    }

    # Construct the request.
    parent = f"projects/{project_id}/locations/global"
    request = dlp_v2.DeidentifyContentRequest(
        parent=parent,
        deidentify_config=deidentify_config,
        item=item,
    )

    # Call the API.
    response = dlp_client.deidentify_content(request=request)

    return response.item.value

if __name__ == "__main__":
    # Example usage:
    # Set your Google Cloud Project ID as an environment variable or replace directly.
    # For example: export GOOGLE_CLOUD_PROJECT_ID="your-project-id"
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")

    if not project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable.")
    else:
        sample_text = "My email is example@example.com and my phone number is 123-456-7890. My name is John Doe."
        redacted_text = redact_unsafe_spans(sample_text, project_id)
        print("Original Text:", sample_text)
        print("Redacted Text:", redacted_text)
