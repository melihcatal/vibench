from google.cloud import dlp_v2


def metric_annotation_safety(text):
    client = dlp_v2.DlpServiceClient()
    parent = f"projects/{client.common_project_path('0')}/locations/global"
    response = client.inspect_content(
        request={
            "parent": parent,
            "item": {"value": text},
            "inspect_config": {"info_types": [{"name": "EMAIL_ADDRESS"}, {"name": "PHONE_NUMBER"}]},
        }
    )
    return {"unsafe": bool(response.result.findings), "findings": [f.info_type.name for f in response.result.findings]}
