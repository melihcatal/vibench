import json
import os
from typing import Any, Dict, List, Optional

import requests


VENDOR_API_HOST = "https://api.veryfi.com"


def _auth_headers() -> Dict[str, str]:
    client_id = os.environ.get("VERYFI_CLIENT_ID", "")
    username = os.environ.get("VERYFI_USERNAME", "")
    api_key = os.environ.get("VERYFI_API_KEY", "")
    if not client_id or not username or not api_key:
        raise ValueError("VERYFI_CLIENT_ID, VERYFI_USERNAME, and VERYFI_API_KEY are required")
    return {
        "CLIENT-ID": client_id,
        "AUTHORIZATION": f"apikey {username}:{api_key}",
    }


def _normalize_line_items(items: Any) -> List[Dict[str, Any]]:
    if not isinstance(items, list):
        return []
    normalized = []
    for item in items:
        if isinstance(item, dict):
            normalized.append(
                {
                    "description": item.get("description") or item.get("name") or item.get("item"),
                    "quantity": item.get("quantity"),
                    "unit_price": item.get("unit_price") or item.get("price"),
                    "amount": item.get("total") or item.get("amount") or item.get("line_total"),
                }
            )
    return normalized


def extract_invoice_fields(invoice_file_path: str) -> Dict[str, Any]:
    url = f"{VENDOR_API_HOST}/api/v8/partner/documents"
    with open(invoice_file_path, "rb") as f:
        response = requests.post(
            url,
            headers=_auth_headers(),
            files={"file": f},
            timeout=60,
        )
    response.raise_for_status()
    payload = response.json()
    vendor = payload.get("vendor") or {}
    date = payload.get("date") or payload.get("invoice_date")
    total = payload.get("total") or payload.get("amount") or payload.get("total_amount")
    line_items = _normalize_line_items(payload.get("line_items") or payload.get("items"))
    return {
        "vendor": vendor.get("name") if isinstance(vendor, dict) else vendor,
        "date": date,
        "total": total,
        "line_items": line_items,
        "raw": payload,
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("invoice_file_path")
    args = parser.parse_args()
    print(json.dumps(extract_invoice_fields(args.invoice_file_path), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
