from google.cloud import dlp_v2
from translation_client import get_project_id


def check_unsafe_content(text: str) -> dict:
    client = dlp_v2.DlpServiceClient()
    project_id = get_project_id()

    # The info types to scan for. See https://cloud.google.com/dlp/docs/infotypes-reference for a complete list.
    info_types = [
        {"name": "EMAIL_ADDRESS"},
        {"name": "PHONE_NUMBER"},
        {"name": "CREDIT_CARD_NUMBER"},
        {"name": "PERSON_NAME"},
        {"name": "US_SOCIAL_SECURITY_NUMBER"},
        {"name": "DATE_OF_BIRTH"},
    ]

    # Construct the `inspect_config` dict. Keys which are not set in the dict
    # will be replaced with a default value. `info_types` is parameter for `inspect_config`
    inspect_config = {
        "info_types": info_types,
        "min_likelihood": dlp_v2.Likelihood.POSSIBLE,
    }

    # Construct the `item` dict. `value` is parameter for `item`
    item = {"value": text}

    parent = f"projects/{project_id}/locations/global"

    response = client.inspect_content(
        request={
            "parent": parent,
            "inspect_config": inspect_config,
            "item": item,
        }
    )

    findings = []
    if response.result.findings:
        for finding in response.result.findings:
            findings.append(
                {
                    "info_type": finding.info_type.name,
                    "likelihood": dlp_v2.Likelihood(finding.likelihood).name,
                    "quote": finding.quote,
                }
            )

    is_safe = not bool(findings)

    return {
        "is_safe": is_safe,
        "findings": findings,
        "dlp_model_used": "Google Cloud DLP API",
    }
