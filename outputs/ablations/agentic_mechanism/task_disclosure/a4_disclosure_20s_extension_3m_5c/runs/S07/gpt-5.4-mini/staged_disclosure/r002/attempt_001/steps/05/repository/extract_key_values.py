import json
import os
import sys
from typing import Any, Dict, List

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def _extract_pairs(result: Any) -> List[Dict[str, Any]]:
    pairs: List[Dict[str, Any]] = []
    for kv in getattr(result, "key_value_pairs", []) or []:
        key = getattr(kv, "key", None)
        value = getattr(kv, "value", None)
        pairs.append(
            {
                "key": getattr(key, "content", None),
                "value": getattr(value, "content", None),
                "key_confidence": getattr(key, "confidence", None),
                "value_confidence": getattr(value, "confidence", None),
            }
        )
    return pairs


def extract_key_values(document_path: str) -> List[Dict[str, Any]]:
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    api_key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_API_KEY"]
    model_id = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_MODEL_ID", "prebuilt-layout")

    client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))

    with open(document_path, "rb") as f:
        poller = client.begin_analyze_document(model_id=model_id, body=f)
        result = poller.result()

    return _extract_pairs(result)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: extract_key_values.py DOCUMENT_PATH")
    output = extract_key_values(sys.argv[1])
    json.dump(output, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
