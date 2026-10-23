from google.cloud import dlp_v2
from security_models import KeyOperationResult

def check_payload_safety(text_payload: str, project_id: str, info_types: list = None) -> KeyOperationResult:
    client = dlp_v2.DlpServiceClient()
    # The project ID to run the API call under.
    # project_id = "YOUR_PROJECT_ID"

    # The string to inspect
    # text_payload = "Larry Page's email is larry@google.com."

    # The infoTypes of information to match
    if info_types is None:
        info_types = [{"name": "EMAIL_ADDRESS"}, {"name": "PHONE_NUMBER"}, {"name": "CREDIT_CARD_NUMBER"}]

    # Construct the `inspect_config` dict
    inspect_config = {"info_types": info_types, "min_likelihood": dlp_v2.Likelihood.POSSIBLE}

    # Construct the `item` dict
    item = {"value": text_payload}

    # Call the API
    try:
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
                findings.append({
                    "info_type": finding.info_type.name,
                    "likelihood": dlp_v2.Likelihood(finding.likelihood).name,
                    "quote": finding.quote,
                })
            return KeyOperationResult(success=True, data={"has_unsafe_content": True, "findings": findings})
        else:
            return KeyOperationResult(success=True, data={"has_unsafe_content": False, "findings": []})

    except Exception as e:
        return KeyOperationResult(success=False, error=str(e))
