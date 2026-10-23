from google.cloud import dlp_v2


def payload_safety(text: str) -> dict:
    client = dlp_v2.DlpServiceClient()
    result = client.deidentify_content(request={"parent": "projects/placeholder/locations/global", "item": {"value": text}})
    return {"provider": "google_dlp", "safe": bool(result.item.value)}
