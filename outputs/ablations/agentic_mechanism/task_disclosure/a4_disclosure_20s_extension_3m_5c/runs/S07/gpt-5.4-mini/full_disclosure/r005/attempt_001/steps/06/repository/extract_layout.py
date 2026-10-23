import os
from typing import Any, Dict, List, Optional

import requests


class AmazonTextractLayoutClient:
    def __init__(self, region: Optional[str] = None, api_key: Optional[str] = None) -> None:
        self.region = region or os.getenv("AWS_REGION", "us-east-1")
        self.api_key = api_key or os.getenv("AWS_ACCESS_KEY_ID")
        self.secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    def extract_layout(self, document_bytes: bytes, features: Optional[List[str]] = None) -> Dict[str, Any]:
        endpoint = f"https://textract.{self.region}.amazonaws.com/"
        headers = {
            "Content-Type": "application/x-amz-json-1.1",
            "X-Amz-Target": "Textract.AnalyzeDocument",
        }
        payload = {
            "Document": {"Bytes": document_bytes.decode("latin1")},
            "FeatureTypes": features or ["LAYOUT", "TABLES", "FORMS"],
        }
        response = requests.post(endpoint, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        blocks = data.get("Blocks", [])
        layout_blocks = [
            block
            for block in blocks
            if block.get("BlockType") in {"LAYOUT_TEXT", "LAYOUT_TITLE", "LAYOUT_SECTION_HEADER", "LAYOUT_TABLE", "LAYOUT_FIGURE", "LINE", "TABLE"}
        ]
        return {"provider": "amazon-textract", "blocks": layout_blocks, "raw": data}


def extract_layout(document_bytes: bytes, features: Optional[List[str]] = None) -> Dict[str, Any]:
    return AmazonTextractLayoutClient().extract_layout(document_bytes=document_bytes, features=features)
