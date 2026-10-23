import os
from typing import List, Dict, Any
import google.cloud.dlp_v2 as dlp


def check_metric_annotations_safety(annotations: List[str]) -> Dict[str, Any]:
    """Check free-text metric labels or annotations for unsafe text using Google Cloud DLP."""

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")

    # Initialize the DLP client
    dlp_client = dlp.DlpServiceClient()

    # Prepare the inspection configuration
    info_types = [
        {"name": "PERSON_NAME"},
        {"name": "EMAIL_ADDRESS"},
        {"name": "PHONE_NUMBER"},
        {"name": "CREDIT_CARD_NUMBER"},
        {"name": "US_SOCIAL_SECURITY_NUMBER"},
        {"name": "IBAN_CODE"},
        {"name": "IP_ADDRESS"},
        {"name": "DATE_OF_BIRTH"},
        {"name": "STREET_ADDRESS"},
    ]

    inspect_config = {
        "info_types": info_types,
        "min_likelihood": dlp.Likelihood.POSSIBLE,
        "include_quote": True,
    }

    # Prepare the content item
    content_item = {"value": "\n".join(annotations)}

    # Create the request
    request = {
        "parent": f"projects/{project_id}",
        "inspect_config": inspect_config,
        "item": content_item,
    }

    # Call the API
    response = dlp_client.inspect_content(request=request)

    # Process results
    findings = []
    if response.result.findings:
        for finding in response.result.findings:
            findings.append(
                {
                    "info_type": finding.info_type.name,
                    "likelihood": finding.likelihood.name,
                    "quote": finding.quote,
                    "location": {
                        "byte_range": {
                            "start": finding.location.byte_range.start,
                            "end": finding.location.byte_range.end,
                        }
                    },
                }
            )

    safety_report = {
        "total_annotations": len(annotations),
        "total_characters": sum(len(a) for a in annotations),
        "findings_count": len(findings),
        "findings": findings,
        "safe": len(findings) == 0,
        "provider": "Google Cloud Data Loss Prevention (DLP)",
    }

    return safety_report


def sanitize_metric_annotation(annotation: str) -> str:
    """Sanitize a metric annotation by removing sensitive information."""

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    dlp_client = dlp.DlpServiceClient()

    # Info types to redact
    info_types = [
        {"name": "PERSON_NAME"},
        {"name": "EMAIL_ADDRESS"},
        {"name": "PHONE_NUMBER"},
        {"name": "CREDIT_CARD_NUMBER"},
        {"name": "US_SOCIAL_SECURITY_NUMBER"},
    ]

    inspect_config = {
        "info_types": info_types,
        "min_likelihood": dlp.Likelihood.POSSIBLE,
    }

    deidentify_config = {
        "info_type_transformations": {
            "transformations": [
                {
                    "primitive_transformation": {
                        "replace_config": {"new_value": {"string_value": "[REDACTED]"}}
                    }
                }
            ]
        }
    }

    item = {"value": annotation}

    request = {
        "parent": f"projects/{project_id}",
        "deidentify_config": deidentify_config,
        "inspect_config": inspect_config,
        "item": item,
    }

    response = dlp_client.deidentify_content(request=request)
    return response.item.value


if __name__ == "__main__":
    test_annotations = [
        "CPU usage for server instance-123",
        "Contact admin at admin@example.com for issues",
        "User John Doe reported high memory usage",
        "Credit card 4111-1111-1111-1111 used for payment",
    ]

    safety_check = check_metric_annotations_safety(test_annotations)
    print(f"Safety check results: {safety_check}")

    sanitized = sanitize_metric_annotation(test_annotations[2])
    print(f"Sanitized annotation: {sanitized}")
