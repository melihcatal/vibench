import json
from typing import List, Dict
from login_audit_store import LoginAuditStore, LoginRecord


def audit_summary(store: LoginAuditStore) -> str:
    """Generate a concise summary of federated login audit events.

    Args:
        store (LoginAuditStore): The document store containing login records.
    Returns:
        str: Human‑readable summary (plain text) that can be sent to monitoring or logs.
    """
    # 1️⃣ Count successful vs failed logins (assuming failures are flagged in profile or status field)
    records: List[LoginRecord] = store.all()
    failed = [r for r in records if not r.profile]
    successful = [r for r in records if r.profile]
    total = len(records)

    lines: List[str] = []
    lines.append(f"Federated Login Audit Summary (Total: {total})")
    lines.append(f" 🚨 Success: {len(successful)}")
    lines.append(f" 🚫 Failure: {len(failed)}")

    # 2️⃣ Top providers by count
    provider_counts: Dict[str, int] = {}
    for r in records:
        provider = r.provider
        provider_counts[provider] = provider_counts.get(provider, 0) + 1
    top_providers = sorted(provider_counts.items(), key=lambda kv: kv[1], reverse=True)[
        :5
    ]
    lines.append(" 📈 Top providers:")
    for provider, cnt in top_providers:
        lines.append(f"   • {provider}: {cnt} logins")

    # 3️⃣ Recent 10 successful logins (including user_id and provider)
    recent = sorted(successful, key=lambda r: r.login_timestamp, reverse=True)[:10]
    lines.append(" 📅 Recent successful logins:")
    for idx, r in enumerate(recent, start=1):
        lines.append(
            f"   {idx}. user_id={r.user_id}, provider={r.provider}, ts={r.login_timestamp}"
        )

    return "\\n".join(lines)


if __name__ == "__main__":
    # Example usage -- requires a configured LoginAuditStore instance
    from identity_client import IdentityClient  # placeholder import only for demo

    # In practice load store from auth config, e.g.:
    # store = LoginAuditStore(uri=MY_CLOUDANT_URL, api_key=MY_API_KEY)
    # print(audit_summary(store))
    print("Initialize LoginAuditStore and call audit_summary(store) to see output.")
