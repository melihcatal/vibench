from google.cloud import dlp_v2

def redact_unsafe(text: str) -> dict:
    dlp_client = dlp_v2.DlpServiceClient()

    # The project ID to run the API call under
    project_id = "your-gcp-project-id"  # Replace with your GCP Project ID
    # The parent resource where the inspection will occur. 
    # A string representing the full resource name of a parent resource.
    # Examples: `projects/project-id` or `projects/project-id/locations/global`
    parent = f"projects/{project_id}/locations/global"

    # Specify the type of info the inspection will look for.
    # For this example, we'll use `PHONE_NUMBER` and `EMAIL_ADDRESS` as examples of "unsafe" data
    # In a real content safety scenario, you might detect other types of sensitive or policy-violating info
    info_types = [{"name": "PHONE_NUMBER"}, {"name": "EMAIL_ADDRESS"}]

    # The item to be redacted
    item = {"value": text}

    # The type of transformation to apply
    redaction_config = {"info_type": {}, "replace_config": {"new_value": {"string_value": "[REDACTED]"}}}

    # Configure the de-identification request
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

    # Perform the de-identification request
    response = dlp_client.deidentify_content(
        request={
            "parent": parent,
            "deidentify_config": deidentify_config,
            "item": item,
        }
    )

    return {
        "original_text": text,
        "redacted_text": response.item.value,
        "provider": "Google Cloud Data Loss Prevention API"
    }

