import os
from google.cloud import dlp_v2
from safety_models import TextModerationRequest, TextModerationResponse
from safety_client import GoogleSafetyClient


def redact_unsafe_content(request: TextModerationRequest) -> TextModerationResponse:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get(
        "GOOGLE_CLOUD_LOCATION", "global"
    )  # DLP is often global or regional

    client = GoogleSafetyClient(project_id, location)
    dlp_parent = client.get_dlp_parent()

    # Configure the types of info to redact
    info_types = [
        {"name": "EMAIL_ADDRESS"},
        {"name": "PHONE_NUMBER"},
        {"name": "CREDIT_CARD_NUMBER"},
        {"name": "US_SOCIAL_SECURITY_NUMBER"},
        {"name": "IP_ADDRESS"},
        {"name": "DATE_OF_BIRTH"},
        {"name": "LOCATION"},
    ]

    # Create a redact action to replace findings with a character (e.g., '*')
    # or a placeholder.
    redact_config = {
        "info_type_transformations": {
            "transformations": [
                {
                    "info_types": info_types,
                    "primitive_transformation": {
                        "character_masking_config": {
                            "masking_character": "*",
                            "number_to_mask": 0,  # Mask all characters
                        }
                    },
                }
            ]
        }
    }

    # Construct the `inspect_config` to specify the info_types to look for
    inspect_config = {
        "info_types": info_types,
        "min_likelihood": dlp_v2.Likelihood.POSSIBLE,
        "limits": {"max_findings_per_request": 0},
    }

    # Construct the `deidentify_config`
    deidentify_config = {
        "info_type_transformations": redact_config["info_type_transformations"]
    }

    # Construct the `item` to be de-identified
    item = {"value": request.text_content}

    # Call the DLP API to de-identify the content
    response = client.dlp_client.deidentify_content(
        request={
            "parent": dlp_parent,
            "deidentify_config": deidentify_config,
            "inspect_config": inspect_config,
            "item": item,
        }
    )

    redacted_text = response.item.value
    is_safe = True if redacted_text == request.text_content else False
    decision_reason = (
        "Content redacted due to sensitive information." if not is_safe else ""
    )

    return TextModerationResponse(
        filtered_text=redacted_text, is_safe=is_safe, decision_reason=decision_reason
    )
