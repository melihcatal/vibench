from typing import Iterable

from google.cloud.dlp_v2 import DlpServiceClient


def metric_annotation_safety(text: str, project_id: str) -> bool:
    client = DlpServiceClient()
    parent = f"projects/{project_id}/locations/global"
    result = client.inspect_content(
        request={
            "parent": parent,
            "item": {"value": text},
            "inspect_config": {
                "info_types": [{"name": "EMAIL_ADDRESS"}, {"name": "PHONE_NUMBER"}]
            },
        }
    )
    return len(result.result.findings) == 0
