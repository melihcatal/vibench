from __future__ import annotations

from observability_client import build_client


def main() -> dict:
    client = build_client()
    result = client.query_errors(severity="ERROR", minutes=120, limit=25)
    return {"filter": result.filter_expression, "messages": result.messages()}
