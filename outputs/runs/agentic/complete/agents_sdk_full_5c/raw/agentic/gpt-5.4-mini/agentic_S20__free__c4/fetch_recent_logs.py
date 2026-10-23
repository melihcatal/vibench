from __future__ import annotations

from observability_client import build_client


def main() -> dict:
    client = build_client()
    result = client.recent(field_name="service", field_value="api", minutes=60, limit=20)
    return {"filter": result.filter_expression, "messages": result.messages()}
