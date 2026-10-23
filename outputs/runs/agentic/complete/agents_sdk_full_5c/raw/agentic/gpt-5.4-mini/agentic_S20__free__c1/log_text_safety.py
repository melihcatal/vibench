from __future__ import annotations

from observability_client import load_datadog_config


def main() -> dict:
    config = load_datadog_config()
    text = "User shared account password in chat"
    unsafe_terms = ["password", "secret", "token", "ssn"]
    matched = [term for term in unsafe_terms if term in text.lower()]
    return {"provider": "datadog", "api_host": config.api_host, "unsafe": bool(matched), "matched": matched}
