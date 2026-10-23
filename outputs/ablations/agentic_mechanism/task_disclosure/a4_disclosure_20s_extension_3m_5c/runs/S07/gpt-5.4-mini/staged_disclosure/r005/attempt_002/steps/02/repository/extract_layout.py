import argparse
import base64
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib import request, error


ADOBE_PDF_SERVICES_EXTRACT_URL = "https://pdf-services.adobe.io/operation/extractpdf"


def _auth_headers() -> Dict[str, str]:
    api_key = os.environ.get("ADOBE_PDF_SERVICES_CLIENT_ID") or os.environ.get("ADOBE_API_KEY")
    if not api_key:
        raise RuntimeError("Missing ADOBE_PDF_SERVICES_CLIENT_ID or ADOBE_API_KEY")
    return {"x-api-key": api_key}


def _read_bytes(path: str) -> bytes:
    return Path(path).expanduser().read_bytes()


def extract_layout(document_path: str) -> Dict[str, Any]:
    payload = {
        "file": base64.b64encode(_read_bytes(document_path)).decode("ascii"),
        "fileName": Path(document_path).name,
        "elements": ["text", "tables", "figures", "charts"],
    }
    data = json.dumps(payload).encode("utf-8")
    headers = _auth_headers()
    headers["content-type"] = "application/json"
    req = request.Request(ADOBE_PDF_SERVICES_EXTRACT_URL, data=data, headers=headers, method="POST")
    try:
        with request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Adobe PDF Services extract failed: {exc.code} {body}") from exc


def _normalize_items(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    items = response.get("elements") or response.get("items") or []
    normalized: List[Dict[str, Any]] = []
    for item in items:
        normalized.append(
            {
                "type": item.get("type") or item.get("kind") or "unknown",
                "text": item.get("text") or item.get("content") or "",
                "bbox": item.get("bbox") or item.get("bounds") or item.get("geometry"),
            }
        )
    return normalized


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract layout elements from a document using Adobe PDF Services.")
    parser.add_argument("document", help="Path to the input document")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()
    result = extract_layout(args.document)
    output = {"provider": "adobe-pdf-services", "layout": _normalize_items(result), "raw": result}
    if args.pretty:
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
