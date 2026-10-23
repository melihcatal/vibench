import os
from datetime import datetime, timezone

import requests


TWILIO_ACCOUNTS_API = "https://api.twilio.com/2010-04-01/Accounts.json"


def _twilio_auth():
    sid = os.environ.get("TWILIO_ACCOUNT_SID")
    token = os.environ.get("TWILIO_AUTH_TOKEN")
    if not sid or not token:
        raise RuntimeError("TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN are required")
    return sid, token


def _fetch_twilio_accounts():
    sid, token = _twilio_auth()
    response = requests.get(TWILIO_ACCOUNTS_API, auth=(sid, token), timeout=30)
    response.raise_for_status()
    payload = response.json()
    return payload.get("accounts", [])


def _rotation_status(account):
    created = account.get("date_created")
    friendly_name = account.get("friendly_name") or account.get("sid")
    status = account.get("status", "unknown")
    if created:
        try:
            created_dt = datetime.strptime(created, "%a, %d %b %Y %H:%M:%S %z")
            age_days = (datetime.now(timezone.utc) - created_dt.astimezone(timezone.utc)).days
        except Exception:
            age_days = None
    else:
        age_days = None
    return {
        "name": friendly_name,
        "status": status,
        "age_days": age_days,
    }


def summarize_secret_rotation():
    accounts = _fetch_twilio_accounts()
    summaries = [_rotation_status(account) for account in accounts]
    if not summaries:
        return "No Twilio accounts found; secret rotation status unavailable."
    lines = ["Twilio secret rotation summary:"]
    for item in summaries:
        age_text = f"{item['age_days']} days old" if item["age_days"] is not None else "age unknown"
        lines.append(f"- {item['name']}: status={item['status']}, {age_text}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(summarize_secret_rotation())
