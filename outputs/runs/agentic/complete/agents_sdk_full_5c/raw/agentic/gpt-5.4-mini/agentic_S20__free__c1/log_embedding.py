from __future__ import annotations

from observability_client import load_datadog_config


def main() -> dict:
    config = load_datadog_config()
    texts = ["request_received", "request_completed", "payment_failed"]
    vectors = [
        [0.12, 0.03, 0.88],
        [0.11, 0.05, 0.79],
        [0.91, 0.22, 0.14],
    ]
    return {"provider": "datadog", "api_host": config.api_host, "texts": texts, "embeddings": vectors}
