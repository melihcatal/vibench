import base64
import json
import os
from typing import Any, Dict, List, Union

import requests


MICROSOFT_DOCINTELLIGENCE_ENDPOINT = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
MICROSOFT_DOCINTELLIGENCE_KEY = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")
MICROSOFT_DOCINTELLIGENCE_MODEL_ID = "prebuilt-receipt"


def _as_json_bytes(receipt_source: Union[str, bytes]) -> bytes:
    if isinstance(receipt_source, bytes):
        return receipt_source
    if os.path.exists(receipt_source):
        with open(receipt_source, "rb") as f:
            return f.read()
    return receipt_source.encode("utf-8")


def _build_request_body(receipt_source: Union[str, bytes]) -> Dict[str, Any]:
    raw = _as_json_bytes(receipt_source)
    return {"base64Source": base64.b64encode(raw).decode("ascii")}


def extract_receipt_fields(receipt_source: Union[str, bytes]) -> Dict[str, Any]:
    if not MICROSOFT_DOCINTELLIGENCE_ENDPOINT or not MICROSOFT_DOCINTELLIGENCE_KEY:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY are required")

    url = f"{MICROSOFT_DOCINTELLIGENCE_ENDPOINT.rstrip('/')}/documentintelligence/documentModels/{MICROSOFT_DOCINTELLIGENCE_MODEL_ID}:analyze?api-version=2024-02-29-preview"
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": MICROSOFT_DOCINTELLIGENCE_KEY,
    }
    response = requests.post(url, headers=headers, json=_build_request_body(receipt_source), timeout=60)
    response.raise_for_status()
    payload = response.json()

    doc = (payload.get("analyzeResult", {}).get("documents") or [{}])[0]
    fields = doc.get("fields", {})

    items: List[Dict[str, Any]] = []
    for item in (fields.get("Items", {}) or {}).get("valueArray", []):
        item_fields = item.get("valueObject", {})
        items.append(
            {
                "description": (item_fields.get("Description", {}) or {}).get("content"),
                "quantity": (item_fields.get("Quantity", {}) or {}).get("content"),
                "totalPrice": (item_fields.get("TotalPrice", {}) or {}).get("content"),
            }
        )

    return {
        "merchant": (fields.get("MerchantName", {}) or {}).get("content"),
        "tax": (fields.get("TotalTax", {}) or {}).get("content"),
        "total": (fields.get("Total", {}) or {}).get("content"),
        "items": items,
        "raw": payload,
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        raise SystemExit("Usage: python extract_receipt_fields.py <receipt_path_or_text>")
    print(json.dumps(extract_receipt_fields(sys.argv[1]), indent=2))
