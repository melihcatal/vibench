from typing import Any, Dict

from google.cloud import dlp_v2


def vendor_text_safety(text: str) -> Dict[str, Any]:
    client = dlp_v2.DlpServiceClient()
    item = {"value": text}
    inspect_config = {"info_types": [{"name": "PERSON_NAME"}, {"name": "EMAIL_ADDRESS"}]}
    response = client.inspect_content(request={"parent": "projects/", "inspect_config": inspect_config, "item": item})
    return {"safe": not response.result.findings, "findings": [finding.info_type.name for finding in response.result.findings]}
