from google.cloud import dlp_v2
from typing import Dict, Any, List
from messaging_models import PubSubMessage
from messaging_client import get_project_id


def check_message_for_unsafe_content(
    message: PubSubMessage, info_types: List[str] = None
) -> Dict[str, Any]:
    """Checks a message payload for unsafe content using Google Cloud DLP API.

    Args:
        message: The PubSubMessage object containing the payload to check.
        info_types: A list of info types to scan for (e.g., ["EMAIL_ADDRESS", "PHONE_NUMBER"]).
                    If None, a default set will be used.

    Returns:
        A dictionary containing the DLP inspection results.
    """
    dlp_client = dlp_v2.DlpServiceClient()
    project_id = get_project_id()

    if info_types is None:
        info_types = [
            "PERSON_NAME",
            "EMAIL_ADDRESS",
            "PHONE_NUMBER",
            "CREDIT_CARD_NUMBER",
        ]

    # Convert message data to a string for DLP inspection
    content_string = str(
        message.data
    )  # Assuming message.data can be reasonably converted to string

    item = {"value": content_string}

    inspect_config = {
        "info_types": [{"name": info_type} for info_type in info_types],
        "min_likelihood": dlp_v2.Likelihood.POSSIBLE,
        "limits": {"max_findings_per_request": 0},  # 0 means unlimited
    }

    parent = f"projects/{project_id}/locations/global"

    response = dlp_client.inspect_content(
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

    return {"findings": findings, "full_response": response.result.to_dict()}
