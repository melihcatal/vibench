from __future__ import annotations

from collections import Counter
from typing import Any

from identity_client import load_oauth_config, fetch_auth0_logs
from identity_models import AuditSummary


def summarize_federated_login_audit(
    query: str = "type:success_login OR type:failed_login",
    page: int = 0,
    per_page: int = 100,
) -> AuditSummary:
    config = load_oauth_config()

    logs = fetch_auth0_logs(
        config=config,
        q=query,
        page=page,
        per_page=per_page,
        sort="-date",
    )

    event_type_counts: dict[str, int] = {}
    connection_counts: dict[str, int] = {}
    ip_counter: Counter = Counter()
    user_subs: set[str] = set()
    failed_logins = 0
    timestamps: list[str] = []

    for entry in logs:
        log_type = entry.get("type", "unknown")
        event_type_counts[log_type] = event_type_counts.get(log_type, 0) + 1

        connection = entry.get("connection", "")
        if connection:
            connection_counts[connection] = connection_counts.get(connection, 0) + 1

        ip = entry.get("ip", "")
        if ip:
            ip_counter[ip] += 1

        user_id = entry.get("user_id", "")
        if user_id:
            user_subs.add(user_id)

        if log_type in ("f", "fl", "failed_login"):
            failed_logins += 1

        log_date = entry.get("date", "")
        if log_date:
            timestamps.append(log_date)

    top_ips = [{"ip": ip, "count": count} for ip, count in ip_counter.most_common(10)]

    time_range_start = min(timestamps) if timestamps else ""
    time_range_end = max(timestamps) if timestamps else ""

    summary = AuditSummary(
        total_events=len(logs),
        unique_users=len(user_subs),
        event_type_counts=event_type_counts,
        connection_counts=connection_counts,
        time_range_start=time_range_start,
        time_range_end=time_range_end,
        top_ips=top_ips,
        failed_logins=failed_logins,
    )

    return summary


if __name__ == "__main__":
    summary = summarize_federated_login_audit()
    print(f"Total events: {summary.total_events}")
    print(f"Unique users: {summary.unique_users}")
    print(f"Failed logins: {summary.failed_logins}")
    print(f"Event types: {summary.event_type_counts}")
