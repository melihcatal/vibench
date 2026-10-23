from google.cloud import dlp_v2


def redact_unsafe(text: str) -> str:
    """Flags or redacts unsafe spans from text using Google Cloud DLP API."""
    client = dlp_v2.DlpServiceClient()
    project = client.project_path(
        "YOUR_PROJECT_ID"
    )  # Replace with your Google Cloud Project ID

    # Configure the types of information to redact. This example uses generic info types.
    # For specific "unsafe" content, you would define custom info types or leverage specific ones.
    info_types = [
        {"name": "PHONE_NUMBER"},
        {"name": "EMAIL_ADDRESS"},
        {"name": "CREDIT_CARD_NUMBER"},
    ]

    # The inspect_config allows you to specify what to look for
    inspect_config = {
        "info_types": info_types,
        "min_likelihood": dlp_v2.Likelihood.POSSIBLE,
    }

    # The redact_config specifies how to redact the findings
    redact_config = {
        "info_type_transformations": [
            {
                "info_types": info_types,
                "transformation": {
                    "replace_config": {"new_value": {"string_value": "[REDACTED]"}}
                },
            }
        ]
    }

    # Request to de-identify content
    response = client.deidentify_content(
        request={
            "parent": project,
            "deidentify_config": {
                "info_type_transformations": redact_config.get(
                    "info_type_transformations"
                )
            },
            "inspect_config": inspect_config,
            "item": {"value": text},
        }
    )
    return response.item.value
