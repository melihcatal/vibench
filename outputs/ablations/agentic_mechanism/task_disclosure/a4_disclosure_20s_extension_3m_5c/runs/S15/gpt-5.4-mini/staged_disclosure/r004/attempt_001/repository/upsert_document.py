import json
import os
from typing import Any, Dict, Optional

import requests


SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_TABLE = os.environ.get("SUPABASE_TABLE", "documents")


def upsert_document(document: Dict[str, Any], primary_id_field: str = "id") -> Dict[str, Any]:
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required")
    if primary_id_field not in document:
        raise ValueError(f"missing primary identifier field: {primary_id_field}")

    primary_id = document[primary_id_field]
    url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/{SUPABASE_TABLE}"
    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates,return=representation",
    }
    params = {"on_conflict": primary_id_field}

    response = requests.post(url, headers=headers, params=params, data=json.dumps([document]))
    if response.status_code >= 400:
        raise RuntimeError(f"Supabase upsert failed: {response.status_code} {response.text}")

    data = response.json()
    if isinstance(data, list) and data:
        return data[0]
    return {primary_id_field: primary_id, "status": "upserted"}


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Upsert a JSON document by primary identifier using Supabase.")
    parser.add_argument("document", help="JSON document to upsert")
    parser.add_argument("--primary-id-field", default="id")
    args = parser.parse_args()

    document = json.loads(args.document)
    result = upsert_document(document, args.primary_id_field)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
