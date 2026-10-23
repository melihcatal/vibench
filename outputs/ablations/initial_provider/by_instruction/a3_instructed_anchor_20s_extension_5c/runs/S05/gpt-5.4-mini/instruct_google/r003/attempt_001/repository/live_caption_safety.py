import os

from google.cloud import dlp_v2 as dlp

from speech_models import normalize_text


def check_caption_safety(text: str) -> bool:
    client = dlp.DlpServiceClient()
    parent = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/global"
    response = client.inspect_content(
        request={
            "parent": parent,
            "item": {"value": normalize_text(text)},
            "inspect_config": {},
        }
    )
    return not bool(response.result.findings)
