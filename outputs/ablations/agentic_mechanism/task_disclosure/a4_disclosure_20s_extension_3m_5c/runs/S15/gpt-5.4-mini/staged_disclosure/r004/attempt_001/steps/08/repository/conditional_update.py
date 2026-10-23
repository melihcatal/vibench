import os
import sys
import requests


BASE_URL = os.getenv("SUPABASE_URL")
API_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
TABLE = os.getenv("SUPABASE_TABLE", "documents")


def update_document(document_id: str, expected_version: int, updates: dict) -> dict:
    if not BASE_URL or not API_KEY:
        raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY or SUPABASE_ANON_KEY are required")
    url = f"{BASE_URL.rstrip('/')}/rest/v1/{TABLE}"
    headers = {
        "apikey": API_KEY,
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
        "If-Match": str(expected_version),
    }
    params = {"id": f"eq.{document_id}", "version": f"eq.{expected_version}"}
    response = requests.patch(url, headers=headers, params=params, json=updates, timeout=30)
    response.raise_for_status()
    return response.json()


def main() -> int:
    if len(sys.argv) < 4:
        return 2
    document_id = sys.argv[1]
    expected_version = int(sys.argv[2])
    field_updates = sys.argv[3:]
    updates = {}
    for item in field_updates:
        key, value = item.split("=", 1)
        updates[key] = value
    result = update_document(document_id, expected_version, updates)
    sys.stdout.write(str(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
