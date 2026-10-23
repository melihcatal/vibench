from typing import List
from google.cloud import dlp_v2
from google.cloud.dlp_v2 import types


def check_log_text_safety(log_messages: List[str]) -> List[dict]:
    """Check log messages for unsafe content using Google Cloud DLP."""
    client = dlp_v2.DlpServiceClient()

    results = []
    for message in log_messages:
        project_id = "your-google-cloud-project"  # Replace with actual project ID

        item = {"value": message}
        inspect_config = {
            "info_types": [
                {"name": "CREDIT_CARD_NUMBER"},
                {"name": "EMAIL_ADDRESS"},
                {"name": "PHONE_NUMBER"},
                {"name": "US_SOCIAL_SECURITY_NUMBER"},
                {"name": "PASSWORD"},
                {"name": "API_KEY"},
            ],
            "min_likelihood": types.Likelihood.POSSIBLE,
        }

        response = client.inspect_content(
            request={
                "parent": f"projects/{project_id}/locations/global",
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
                        "likelihood": finding.likelihood.name,
                        "quote": finding.quote,
                    }
                )

        results.append({"message": message, "findings": findings})

    return results
