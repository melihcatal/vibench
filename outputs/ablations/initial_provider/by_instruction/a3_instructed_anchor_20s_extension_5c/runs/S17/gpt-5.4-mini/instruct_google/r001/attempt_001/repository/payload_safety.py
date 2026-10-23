from google.cloud import dlp_v2

from security_models import normalize_text


def payload_safety(text: str) -> dict:
    client = dlp_v2.DlpServiceClient()
    result = client.inspect_content(request={"parent": "projects/placeholder/locations/global", "item": {"value": normalize_text(text)}})
    return {"provider": "google_cloud_dlp", "findings": len(result.result.findings), "safe": len(result.result.findings) == 0}
