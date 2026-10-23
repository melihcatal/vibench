from google.cloud import dlp_v2
import os

def redact_unsafe(project_id: str, text: str) -> dict:
    """
    Flags or redacts unsafe spans from text using Google Cloud Data Loss Prevention (DLP) API.
    """
    dlp = dlp_v2.DlpServiceClient()

    # The info_types for unsafe content might vary.
    # Commonly used ones for general safety include:
    # "PERSON_NAME", "EMAIL_ADDRESS", "PHONE_NUMBER", "CREDIT_CARD_NUMBER"
    # For more advanced content safety, consider custom info types or
    # combining with other moderation services to identify unsafe content first.
    info_types = [
        {"name": "PHONE_NUMBER"},
        {"name": "EMAIL_ADDRESS"},
        {"name": "CREDIT_CARD_NUMBER"},
        {"name": "PERSON_NAME"},
        # Add other relevant info types for redaction based on your definition of "unsafe spans"
        # For example, if you consider hate speech or violent language as "unsafe spans"
        # that need redaction, you might need a pre-analysis step with a content moderation API
        # to identify those spans and then feed them to DLP for generic redaction.
    ]

    # Specify how to redact (e.g., replace with "[[REDACTED]]")
    redaction_config = dlp_v2.RedactImageRequest.ImageRedactionConfig(
        redaction_color=dlp_v2.Color(red=0.0, green=0.0, blue=0.0),
        info_type=dlp_v2.InfoType(name="ALL_TEXT") # This will redact all text found by info_types
    )

    # For text redaction, use `deidentify_content`
    item = {"value": text}
    deidentify_config = {
        "info_type_transformations": {
            "transformations": [
                {
                    "info_types": info_types,
                    "primitive_transformation": {"replace_config": {"new_value": {"string_value": "[REDACTED]"}}},
                }
            ]
        }
    }

    parent = f"projects/{project_id}"
    response = dlp.deidentify_content(
        request={"parent": parent, "deidentify_config": deidentify_config, "item": item}
    )

    return {"original_text": text, "redacted_text": response.item.value}

if __name__ == '__main__':
    # Replace with your Google Cloud Project ID
    project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id") 
    
    if project_id == "your-gcp-project-id":
        print("WARNING: Please set the GCP_PROJECT_ID environment variable or update the script with your actual project ID.")
        print("Using a placeholder project ID, which will likely fail without proper authentication/configuration.")

    example_text = "My name is John Doe, my email is john.doe@example.com, and my number is 123-456-7890. My credit card is 1234-5678-9012-3456."
    redaction_output = redact_unsafe(project_id, example_text)
    print(f"Original Text: {redaction_output['original_text']}")
    print(f"Redacted Text: {redaction_output['redacted_text']}")

    example_text_safe = "This is a safe message without sensitive information."
    redaction_output_safe = redact_unsafe(project_id, example_text_safe)
    print(f"\nOriginal Text: {redaction_output_safe['original_text']}")
    print(f"Redacted Text: {redaction_output_safe['redacted_text']}")
