from google.cloud import dlp_v2 as dlp

from document_models import normalize_text


def check_ocr_safety(text: str, project_id: str, inspect_template_name: str = ""):
    client = dlp.DlpServiceClient()
    parent = f"projects/{project_id}"
    item = {"value": normalize_text(text)}
    request = {"parent": parent, "item": item}
    if inspect_template_name:
        request["inspect_template_name"] = inspect_template_name
    response = client.inspect_content(request=request)
    return {"findings": [finding.info_type.name for finding in getattr(response.result, "findings", [])]}
