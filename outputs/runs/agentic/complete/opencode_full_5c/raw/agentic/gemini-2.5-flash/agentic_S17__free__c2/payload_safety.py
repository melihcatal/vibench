from security_client import SecurityClient
from security_models import PayloadSafetyRequest
from google.cloud import dlp_v2


def check_payload_safety(request: PayloadSafetyRequest) -> dict:
    client = SecurityClient()

    # The inspect_content request to be sent to the DLP API
    dlp_request = {
        "parent": f"projects/{request.project_id}/locations/global",
        "inspect_config": {
            "info_types": [
                {"name": "EMAIL_ADDRESS"},
                {"name": "PHONE_NUMBER"},
                {"name": "CREDIT_CARD_NUMBER"},
            ],
            "min_likelihood": dlp_v2.Likelihood.POSSIBLE,
        },
        "item": {"value": request.text_content},
    }

    response = client.dlp_client.inspect_content(request=dlp_request)

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

    return {"findings": findings}
