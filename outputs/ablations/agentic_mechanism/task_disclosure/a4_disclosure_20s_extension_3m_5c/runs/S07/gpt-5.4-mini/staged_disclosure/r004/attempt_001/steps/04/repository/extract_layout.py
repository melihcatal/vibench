import argparse
import json
import os
from pathlib import Path

import requests


MICROSOFT_AZURE_FORM_RECOGNIZER_ENDPOINT = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
MICROSOFT_AZURE_FORM_RECOGNIZER_KEY = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")
MICROSOFT_AZURE_FORM_RECOGNIZER_API_VERSION = "2024-02-29-preview"


def extract_layout(document_path: str):
    if not MICROSOFT_AZURE_FORM_RECOGNIZER_ENDPOINT or not MICROSOFT_AZURE_FORM_RECOGNIZER_KEY:
        raise RuntimeError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY are required")

    path = Path(document_path)
    if not path.is_file():
        raise FileNotFoundError(document_path)

    url = (
        MICROSOFT_AZURE_FORM_RECOGNIZER_ENDPOINT.rstrip("/")
        + "/documentintelligence/documentModels/prebuilt-layout:analyze?api-version="
        + MICROSOFT_AZURE_FORM_RECOGNIZER_API_VERSION
    )

    headers = {
        "Ocp-Apim-Subscription-Key": MICROSOFT_AZURE_FORM_RECOGNIZER_KEY,
        "Content-Type": "application/octet-stream",
    }

    with path.open("rb") as f:
        response = requests.post(url, headers=headers, data=f.read(), timeout=120)
    response.raise_for_status()

    operation_location = response.headers.get("operation-location") or response.headers.get("Operation-Location")
    if not operation_location:
        return response.json()

    poll_headers = {"Ocp-Apim-Subscription-Key": MICROSOFT_AZURE_FORM_RECOGNIZER_KEY}
    while True:
        poll_response = requests.get(operation_location, headers=poll_headers, timeout=120)
        poll_response.raise_for_status()
        payload = poll_response.json()
        status = payload.get("status")
        if status in {"succeeded", "failed", "canceled"}:
            return payload


def main():
    parser = argparse.ArgumentParser(description="Extract layout elements from a document using Azure Document Intelligence.")
    parser.add_argument("document", help="Path to the document to analyze")
    parser.add_argument("--output", help="Optional path to write JSON output")
    args = parser.parse_args()

    result = extract_layout(args.document)
    output = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
