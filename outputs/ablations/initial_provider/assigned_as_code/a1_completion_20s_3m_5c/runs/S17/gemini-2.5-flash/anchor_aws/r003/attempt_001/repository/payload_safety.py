from google.cloud import dlp_v2

def check_payload_safety(project_id: str, text_payload: str, info_types: list = None):
    client = dlp_v2.DlpServiceClient()
    if info_types is None:
        info_types = [{"name": "EMAIL_ADDRESS"}, {"name": "PHONE_NUMBER"}, {"name": "CREDIT_CARD_NUMBER"}]

    # Construct the `inspect_config` containing the information types (medical codes).
    inspect_config = {"info_types": info_types, "min_likelihood": dlp_v2.Likelihood.POSSIBLE}

    # Construct the `item` to be inspected.
    item = {"value": text_payload}

    # Call the API to inspect the content.
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
                "quote": finding.quote
            })
    return {"findings": findings}