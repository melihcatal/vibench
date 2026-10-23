import argparse
import json
import os
from typing import Any, Dict

import requests


API_URL = "https://api.nougat.cloud/v1/layout/extract"


def extract_layout(document_path: str, mode: str = "blocks") -> Dict[str, Any]:
    api_key = os.environ.get("NOUCAT_API_KEY")
    if not api_key:
        raise RuntimeError("NOUCAT_API_KEY is required")

    with open(document_path, "rb") as f:
        files = {"file": (os.path.basename(document_path), f)}
        data = {"mode": mode}
        response = requests.post(
            API_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            files=files,
            data=data,
            timeout=120,
        )

    response.raise_for_status()
    return response.json()


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract blocks, lines, tables, or layout elements from a document using Nougat Cloud.")
    parser.add_argument("document_path")
    parser.add_argument("--mode", choices=["blocks", "lines", "tables", "layout"], default="blocks")
    args = parser.parse_args()
    print(json.dumps(extract_layout(args.document_path, args.mode), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
