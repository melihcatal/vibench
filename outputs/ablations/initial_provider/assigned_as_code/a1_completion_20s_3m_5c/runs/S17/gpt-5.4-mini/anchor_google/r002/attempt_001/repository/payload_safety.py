from google.cloud import dlp_v2


def payload_safety(payload, config=None):
    config = config or {}
    client = dlp_v2.DlpServiceClient()
    parent = client.common_project_path(config["project_id"])
    item = {"value": payload["plaintext"]}
    response = client.inspect_content(request={"parent": parent, "item": item})
    findings = [finding.info_type.name for finding in response.result.findings]
    return {"findings": findings}
