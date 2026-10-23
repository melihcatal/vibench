from google.cloud import dlp_v2


def check_script_safety(text: str, project_id: str, location: str = "global") -> bool:
    client = dlp_v2.DlpServiceClient()
    parent = f"projects/{project_id}/locations/{location}"
    item = dlp_v2.ContentItem(value=text)
    response = client.deidentify_content(request={"parent": parent, "item": item, "deidentify_config": {"info_type_transformations": {"transformations": []}}})
    return bool(response)
