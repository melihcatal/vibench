from google.cloud import dlp_v2 as dlp

def check_text_safety_dlp(text: str, project_id: str) -> dict:
    client = dlp.DlpServiceClient()
    # The INFO_TYPES_NAME values can be found at:
    # https://cloud.google.com/dlp/docs/infotypes-reference
    info_types = [{"name": "PHONE_NUMBER"}, {"name": "EMAIL_ADDRESS"}, {"name": "CREDIT_CARD_NUMBER"}]

    # Construct the `inspect_config` dict. Keys which are omitted are
    # treated as default. See documentation for more info.
    inspect_config = {
        "info_types": info_types,
        "min_likelihood": dlp.Likelihood.POSSIBLE,
        "limits": {"max_findings_per_request": 0},
    }

    # Construct the `item` dict
    item = {"value": text}

    # Convert the project id into a full resource id.
    parent = f"projects/{project_id}/locations/global"

    # Call the API
    response = client.inspect_content(request={'parent': parent, 'inspect_config': inspect_config, 'item': item})

    if response.result.findings:
        return {"unsafe_content_detected": True, "findings": [f.info_type.name for f in response.result.findings]}
    else:
        return {"unsafe_content_detected": False, "findings": []}
