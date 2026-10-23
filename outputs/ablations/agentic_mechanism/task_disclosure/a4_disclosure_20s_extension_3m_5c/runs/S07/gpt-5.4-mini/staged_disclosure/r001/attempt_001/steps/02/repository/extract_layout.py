import argparse
import base64
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from urllib import request, error


AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "").rstrip("/")
AZURE_DOCUMENT_INTELLIGENCE_API_KEY = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_API_KEY", "")
AZURE_DOCUMENT_INTELLIGENCE_API_VERSION = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_API_VERSION", "2024-02-29-preview")
AZURE_DOCUMENT_INTELLIGENCE_MODEL = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_MODEL", "prebuilt-layout")


def _read_input(source: str) -> bytes:
    if source.startswith("http://") or source.startswith("https://"):
        with request.urlopen(source) as resp:
            return resp.read()
    return Path(source).read_bytes()


def extract_layout(source: str, output: Optional[str] = None) -> Dict[str, Any]:
    if not AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT or not AZURE_DOCUMENT_INTELLIGENCE_API_KEY:
        raise RuntimeError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_API_KEY are required")

    data = _read_input(source)
    analyze_url = f"{AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT}/documentintelligence/documentModels/{AZURE_DOCUMENT_INTELLIGENCE_MODEL}:analyze?api-version={AZURE_DOCUMENT_INTELLIGENCE_API_VERSION}"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_DOCUMENT_INTELLIGENCE_API_KEY,
        "Content-Type": "application/pdf" if source.lower().endswith(".pdf") else "application/octet-stream",
    }
    req = request.Request(analyze_url, data=data, headers=headers, method="POST")
    try:
        with request.urlopen(req) as resp:
            operation_location = resp.headers.get("Operation-Location")
    except error.HTTPError as exc:
        raise RuntimeError(exc.read().decode("utf-8", "ignore")) from exc

    if not operation_location:
        raise RuntimeError("Missing Operation-Location header from Azure Document Intelligence")

    poll_headers = {"Ocp-Apim-Subscription-Key": AZURE_DOCUMENT_INTELLIGENCE_API_KEY}
    result: Dict[str, Any] = {}
    for _ in range(120):
        poll_req = request.Request(operation_location, headers=poll_headers, method="GET")
        with request.urlopen(poll_req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        status = result.get("status")
        if status in {"succeeded", "failed", "canceled"}:
            break
    if result.get("status") != "succeeded":
        raise RuntimeError(json.dumps(result, indent=2))

    if output:
        Path(output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract layout elements from a document using Azure Document Intelligence")
    parser.add_argument("source")
    parser.add_argument("--output")
    args = parser.parse_args()
    extract_layout(args.source, args.output)


if __name__ == "__main__":
    main()
