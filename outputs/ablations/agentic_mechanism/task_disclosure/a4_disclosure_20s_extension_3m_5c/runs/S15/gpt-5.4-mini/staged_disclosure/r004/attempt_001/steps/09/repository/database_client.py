import os
from typing import Any, Dict, Optional

import requests


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_TABLE = os.getenv("SUPABASE_TABLE", "documents")


def get_database_config() -> Dict[str, Optional[str]]:
    return {
        "url": SUPABASE_URL,
        "service_role_key": SUPABASE_SERVICE_ROLE_KEY,
        "anon_key": SUPABASE_ANON_KEY,
        "table": SUPABASE_TABLE,
    }


def get_client() -> requests.Session:
    if not SUPABASE_URL:
        raise RuntimeError("SUPABASE_URL is required")
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    api_key = SUPABASE_SERVICE_ROLE_KEY or SUPABASE_ANON_KEY
    if api_key:
        session.headers.update({"apikey": api_key, "Authorization": f"Bearer {api_key}"})
    return session


def table_url(table_name: Optional[str] = None) -> str:
    if not SUPABASE_URL:
        raise RuntimeError("SUPABASE_URL is required")
    return f"{SUPABASE_URL.rstrip('/')}/rest/v1/{table_name or SUPABASE_TABLE}"


def build_select_params(filters: Optional[Dict[str, Any]] = None, select: str = "*") -> Dict[str, str]:
    params = {"select": select}
    if filters:
        for key, value in filters.items():
            params[key] = f"eq.{value}"
    return params


def list_documents(filters: Optional[Dict[str, Any]] = None, table_name: Optional[str] = None, limit: int = 100) -> Any:
    session = get_client()
    params = build_select_params(filters)
    params["limit"] = str(limit)
    response = session.get(table_url(table_name), params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_document(document_id: str, id_field: str = "id", table_name: Optional[str] = None) -> Dict[str, Any]:
    if not document_id:
        raise ValueError("document_id is required")
    session = get_client()
    params = {"select": "*", id_field: f"eq.{document_id}", "limit": "1"}
    response = session.get(table_url(table_name), params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    if isinstance(data, list) and data:
        return data[0]
    raise KeyError(f"Document not found for identifier: {document_id}")


def upsert_document(document: Dict[str, Any], primary_id_field: str = "id", table_name: Optional[str] = None) -> Any:
    if primary_id_field not in document:
        raise ValueError(f"missing primary identifier field: {primary_id_field}")
    session = get_client()
    response = session.post(
        table_url(table_name),
        params={"on_conflict": primary_id_field},
        headers={"Prefer": "resolution=merge-duplicates,return=representation"},
        json=[document],
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data[0] if isinstance(data, list) and data else {primary_id_field: document[primary_id_field], "status": "upserted"}
