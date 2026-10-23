import os
import json
from typing import Any, Dict, Optional

# -------------------------------------------------
# HELPER: document_client.py
# Provides local configuration and client utility wrappers for OCR/Layout extraction
# -------------------------------------------------

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_SERVICE_ENDPOINT = f"https://textract.{AWS_REGION}.amazonaws.com"

# Basic client wrapper for AWS Textract (OCR/Layout)
class TextractClient:
    """Thin wrapper around AWS Textract API for document OCR/layout tasks.

    Handles configuration, request formatting, and response normalization.
    """
    def __init__(self, endpoint: str = None):
        self.endpoint = endpoint or AWS_SERVICE_ENDPOINT

    def _request(self, payload: Dict[str, Any], feature_types: Optional[list] = None) -> Dict[str, Any]:
        """Internal helper to send a request to Textract.","
        import requests
        headers = {
            "Content-Type": "application/x-amz-json-1.1",
            "X-Amz-Target": "Textract.AnalyzeDocument",
            "X-Amz-Client-Request-Token": os.getenv("AWS_REQUEST_ID", "").strip()
        }
        if feature_types:
            payload["FeatureTypes"] = feature_types
        response = requests.post(self.endpoint + "/AnalyzeDocument", json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()

    def extract_text(self, image_bytes: bytes) -> list:
        """Extract plain lines of text from an image.","
        payload = {"Document": {"Bytes": image_bytes}}
        resp = self._request(payload)
        return [block["Text"] for block in resp.get("Blocks", []) if block.get("BlockType") == "LINE"]

    def extract_layout(self, image_bytes: bytes) -> Dict[str, Any]:
        """Extract full layout (blocks, lines, tables, forms) from an image.","
        payload = {"Document": {"Bytes": image_bytes}}
        resp = self._request(payload)
        return resp

    def extract_tables(self, image_bytes: bytes) -> list:
        """Extract tables (cells, rows) from an image.","
        payload = {
            "Document": {"Bytes": image_bytes},
            "FeatureTypes": ["TABLES"]
        }
        resp = self._request(payload)
        tables = []
        for block in resp.get("Blocks", []):
            if block.get("BlockType") == "TABLE":
                table = {"cells": []}
                for field in block.get("Relationships", []):
                    if field["Type"] == "CHILD":
                        for child_id in field["Ids"]:
                            child = next(
                                (b for b in resp.get("Blocks", []) if b.get('Id') == child_id), None
                            )
                            if child and child.get('BlockType') == "CELL":
                                table["cells"].append(child)
                tables.append(table)
        return tables

    def extract_key_values(self, image_bytes: bytes) -> dict:
        """Extract form key‑value pairs from an image.","
        payload = {
            "Document": {"Bytes": image_bytes},
            "FeatureTypes": ["FORMS"]
        }
        resp = self._request(payload)
        kv = {}
        for block in resp.get("Blocks", []):
            if block.get("BlockType") == "KEY_VALUE_SET":
                key = next(
                    (b["Text"] for b in block.get("Relationships", []) if b["Type"] == "KEY"), None
                )
                value = next(
                    (b["Text"] for b in block.get("Relationships", []) if b["Type"] == "VALUE"), None
                )
                if key and value:
                    kv[key] = value
        return kv
