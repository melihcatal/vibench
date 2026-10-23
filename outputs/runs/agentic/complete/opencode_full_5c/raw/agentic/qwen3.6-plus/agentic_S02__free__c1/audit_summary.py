import os
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone

from identity_models import AuditEvent, serialize_audit_events


SPLUNK_HOST = os.environ.get("SPLUNK_HOST", "https://api.splunk.com")
SPLUNK_PORT = os.environ.get("SPLUNK_PORT", "8089")
SPLUNK_INDEX = os.environ.get("SPLUNK_INDEX", "federated_login")


def query_splunk_audit_events(
    search_query: str,
    earliest: Optional[str] = None,
    latest: Optional[str] = None,
    splunk_host: Optional[str] = None,
    splunk_port: Optional[str] = None,
    splunk_token: Optional[str] = None,
    max_results: int = 1000,
) -> List[Dict[str, Any]]:
    import requests

    host = splunk_host or SPLUNK_HOST
    port = splunk_port or SPLUNK_PORT
    token = splunk_token or os.environ.get("SPLUNK_ACCESS_TOKEN", "")

    base_url = f"{host}:{port}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    search_params = {
        "search": f"search index={SPLUNK_INDEX} {search_query}",
        "output_mode": "json",
        "count": max_results,
    }
    if earliest:
        search_params["earliest_time"] = earliest
    if latest:
        search_params["latest_time"] = latest

    resp = requests.get(
        f"{base_url}/services/search/jobs/export",
        headers=headers,
        params=search_params,
        timeout=60,
    )
    resp.raise_for_status()

    results = []
    for line in resp.text.strip().split("\n"):
        if line:
            try:
                result = __import__("json").loads(line)
                if "result" in result:
                    results.append(result["result"])
            except __import__("json").JSONDecodeError:
                continue

    return results


def summarize_federated_login_events(
    time_range_hours: int = 24,
    splunk_host: Optional[str] = None,
    splunk_port: Optional[str] = None,
    splunk_token: Optional[str] = None,
) -> Dict[str, Any]:
    now = datetime.now(timezone.utc)
    earliest = (
        now.replace(hour=0, minute=0, second=0, microsecond=0).replace(
            hour=now.hour - time_range_hours
        )
    ).isoformat()
    latest = now.isoformat()

    events = query_splunk_audit_events(
        search_query="sourcetype=federated_login",
        earliest=earliest,
        latest=latest,
        splunk_host=splunk_host,
        splunk_port=splunk_port,
        splunk_token=splunk_token,
    )

    total_events = len(events)
    success_count = sum(1 for e in events if e.get("status") == "success")
    failure_count = sum(1 for e in events if e.get("status") in ("failure", "error"))

    provider_counts: Dict[str, int] = {}
    for e in events:
        p = e.get("provider", "unknown")
        provider_counts[p] = provider_counts.get(p, 0) + 1

    error_reasons: Dict[str, int] = {}
    for e in events:
        if e.get("status") in ("failure", "error"):
            reason = e.get("error_reason", e.get("details", {}).get("error", "unknown"))
            error_reasons[reason] = error_reasons.get(reason, 0) + 1

    unique_users = len({e.get("user_sub") for e in events if e.get("user_sub")})

    return {
        "summary_period": {
            "earliest": earliest,
            "latest": latest,
            "hours": time_range_hours,
        },
        "total_events": total_events,
        "success_count": success_count,
        "failure_count": failure_count,
        "success_rate": round(success_count / total_events, 4)
        if total_events > 0
        else 0.0,
        "unique_users": unique_users,
        "events_by_provider": provider_counts,
        "error_breakdown": error_reasons,
        "provider": "splunk",
        "splunk_host": splunk_host or SPLUNK_HOST,
        "splunk_index": SPLUNK_INDEX,
    }


def generate_audit_report(
    time_range_hours: int = 24,
    group_by: str = "provider",
    splunk_host: Optional[str] = None,
    splunk_port: Optional[str] = None,
    splunk_token: Optional[str] = None,
) -> Dict[str, Any]:
    summary = summarize_federated_login_events(
        time_range_hours=time_range_hours,
        splunk_host=splunk_host,
        splunk_port=splunk_port,
        splunk_token=splunk_token,
    )

    events = query_splunk_audit_events(
        search_query=f"sourcetype=federated_login | stats count by {group_by}",
        splunk_host=splunk_host,
        splunk_port=splunk_port,
        splunk_token=splunk_token,
    )

    grouped_stats = {}
    for e in events:
        key = e.get(group_by, "unknown")
        grouped_stats[key] = int(e.get("count", 0))

    summary["grouped_by"] = group_by
    summary["grouped_stats"] = grouped_stats

    return summary
