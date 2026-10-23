import os
from typing import Any, Dict, Optional

from supabase import Client, create_client


SUPABASE_URL_ENV = "SUPABASE_URL"
SUPABASE_SERVICE_ROLE_ENV = "SUPABASE_SERVICE_ROLE_KEY"
SUPABASE_TABLE_ENV = "SUPABASE_EXPENSE_RECORDS_TABLE"


def _get_env(name: str, fallback: Optional[str] = None) -> str:
    value = os.getenv(name, fallback)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def get_expense_record_store_client() -> Client:
    url = _get_env(SUPABASE_URL_ENV)
    key = _get_env(SUPABASE_SERVICE_ROLE_ENV)
    return create_client(url, key)


def get_expense_record_table() -> str:
    return os.getenv(SUPABASE_TABLE_ENV, "expense_records")


def persist_expense_record(record: Dict[str, Any]) -> Dict[str, Any]:
    client = get_expense_record_store_client()
    table = get_expense_record_table()
    response = client.table(table).insert(record).execute()
    data = getattr(response, "data", None)
    if not data:
        raise RuntimeError("Failed to persist expense record in Supabase")
    return data[0]


def upsert_expense_record(record: Dict[str, Any], conflict_target: str = "id") -> Dict[str, Any]:
    client = get_expense_record_store_client()
    table = get_expense_record_table()
    response = client.table(table).upsert(record, on_conflict=conflict_target).execute()
    data = getattr(response, "data", None)
    if not data:
        raise RuntimeError("Failed to upsert expense record in Supabase")
    return data[0]
