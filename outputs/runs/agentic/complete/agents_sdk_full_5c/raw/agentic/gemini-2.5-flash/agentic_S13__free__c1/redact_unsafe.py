import os
from google.cloud import dlp_v2

def redact_unsafe(text: str, info_types: list[str] = None) -> dict:
    """
    Flags or redacts unsafe spans from text using Google Cloud Data Loss Prevention (DLP) API.
    """
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")

    dlp_client = dlp_v2.DlpServiceClient()

    if info_types is None:
        # Default info types for common sensitive data, adjust as needed for 'unsafe' content
        # DLP is more about PII/sensitive data, not general 'unsafe' content like hate speech.
        # To align with 'unsafe spans', we can use custom info types or a broader set if applicable.
        # For this example, we'll use some standard info types that could be considered 'unsafe' contextually,
        # or more accurately, sensitive and often needing redaction in a safety context.
        info_types = [
            "EMAIL_ADDRESS",
            "PHONE_NUMBER",
            "CREDIT_CARD_NUMBER",
            "IP_ADDRESS",
            "GENERIC_PII" # This is a placeholder for a broader PII category
        ]

    # Convert string info types to InfoType objects
    inspect_config_info_types = [{'name': info_type} for info_type in info_types]

    inspect_config = {"info_types": inspect_config_info_types, "min_likelihood": dlp_v2.Likelihood.POSSIBLE}
    redact_config = {"info_type_name": True}

    # For redacting, we use deidentify_content. For flagging, we would use inspect_content.
    deidentify_config = {"info_type_transformations": {"transformations": [{
        "info_types": inspect_config_info_types,
        "primitive_transformation": {"redact_config": {}}
    }]}}

    item = {"value": text}

    parent = f"projects/{project_id}/locations/global"

    response = dlp_client.deidentify_content(
        request={
            "parent": parent,
            "deidentify_config": deidentify_config,
            "inspect_config": inspect_config,
            "item": item
        }
    )

    redacted_text = response.item.value
    return {"original_text": text, "redacted_text": redacted_text, "source": "Google Cloud DLP"}

if __name__ == "__main__":
    test_text = "My email is test@example.com and my phone is 123-456-7890. This is unsafe content."
    result = redact_unsafe(test_text)
    print(f"Redaction result for \"{test_text}\"")
    print(result)

    custom_info_types_text = "My secret code is XYZ123 and I will meet you at 123 Main St."
    # Note: For custom info types like 'secret code', you'd define custom detectors in DLP.
    # This example only uses built-in ones. For a true 'unsafe content' redaction beyond PII,
    # a combination with moderation and custom regex/dictionaries would be needed.
    result_custom = redact_unsafe(custom_info_types_text, info_types=["STREET_ADDRESS"])
    print(f"Redaction result for \"{custom_info_types_text}\" with custom info types")
    print(result_custom)
