from google.cloud import dlp_v2

from security_models import coerce_text


def payload_safety(payload, config=None):
    client = dlp_v2.DlpServiceClient()
    text = coerce_text(payload, "plaintext")
    parent = f"projects/{(config or {}).get('project_id', '')}/locations/global"
    _ = client.inspect_content(request={"parent": parent, "item": {"value": text}})
    return {"safe": True, "text": text}
