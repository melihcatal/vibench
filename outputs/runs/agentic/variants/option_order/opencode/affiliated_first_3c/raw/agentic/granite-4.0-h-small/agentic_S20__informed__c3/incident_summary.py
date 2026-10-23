import os
import json
from datetime import datetime
from observability_client import ManagedLogClient
from observability_models import LogEntry, LogSearchResult


def incident_summary(
    severity: str = "error",
    start_time: datetime | None = None,
    end_time: datetime | None = None,
) -> str:
    """Summarize error‑log findings for incident review.

    Uses Granite via watsonx.ai as the concrete provider for summarization.
    """
    # 1️⃣ Pull recent error logs
    client = ManagedLogClient()
    logs = client.query_logs(
        filter_expr=f'resource.type="global" AND severity="{severity}"'
    )
    # Convert to simplified list of dicts for the LLM
    log_dicts = [
        {"timestamp": str(l["timestamp"]), "level": l["level"], "msg": l["message"]}
        for l in logs
    ]
    # 2️⃣ Build prompt for Granite
    prompt = f"Summarize the following {len(log_dicts)} error logs for incident review. Include a brief description, the most frequent error codes, and any actionable items.\n\nLogs:\n{json.dumps(log_dicts, indent=2)}"
    # 3️⃣ Call Granite inference (using ibm-watsonx-ai SDK)
    summary = _run_granite(prompt)
    return summary["text"]


def _run_granite(prompt: str) -> dict:
    # Placeholder implementation – in real code you would invoke the watsonx.ai SDK
    # Example:
    # from ibm_watsonx_ai import Client
    # client = Client(...)
    # response = client.text_generation.create_response(...)
    # Here we simulate a response.
    return {"text": f"SUMMARY: {prompt[:60]}... (truncated for demo)"}
