from google.cloud import dlp_v2
from security_client import get_dlp_client, PROJECT_ID
from security_models import PayloadSafetyRequest, PayloadSafetyResponse


def check_payload_safety(request: PayloadSafetyRequest) -> PayloadSafetyResponse:
    client = get_dlp_client()
    dlp_project_id = request.project_id if request.project_id else PROJECT_ID
    project_path = f"projects/{dlp_project_id}"

    # Configure the inspect content request
    item = {"value": request.text_payload}
    inspect_config = {
        "info_types": [
            {"name": "EMAIL_ADDRESS"},
            {"name": "PHONE_NUMBER"},
            {"name": "CREDIT_CARD_NUMBER"},
            {"name": "US_SOCIAL_SECURITY_NUMBER"},
        ],
        "min_likelihood": dlp_v2.Likelihood.POSSIBLE,
        "limits": {"max_findings_per_request": 0},
    }

    # Call the DLP API to inspect the content
    response = client.inspect_content(
        request={
            "parent": project_path,
            "inspect_config": inspect_config,
            "item": item,
        }
    )

    has_sensitive_content = False
    findings_list = []

    if response.result.findings:
        has_sensitive_content = True
        for finding in response.result.findings:
            findings_list.append(
                {
                    "info_type": finding.info_type.name,
                    "likelihood": dlp_v2.Likelihood(finding.likelihood).name,
                    "quote": finding.quote,
                }
            )

    return PayloadSafetyResponse(
        has_sensitive_content=has_sensitive_content, findings=findings_list
    )
