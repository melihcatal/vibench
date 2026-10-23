import os
from datetime import datetime, timedelta, timezone

import requests


def query_error_logs(severity: str, minutes_back: int, limit: int = 50):
    api_key = os.environ.get("NEW_RELIC_API_KEY")
    account_id = os.environ.get("NEW_RELIC_ACCOUNT_ID")
    if not api_key or not account_id:
        raise ValueError("NEW_RELIC_API_KEY and NEW_RELIC_ACCOUNT_ID are required")

    since = datetime.now(timezone.utc) - timedelta(minutes=minutes_back)
    until = datetime.now(timezone.utc)
    nrql = (
        "SELECT timestamp, message, severity FROM Log "
        f"WHERE severity = '{severity}' "
        f"SINCE '{since.isoformat()}' UNTIL '{until.isoformat()}' "
        f"LIMIT {int(limit)}"
    )

    response = requests.post(
        f"https://api.newrelic.com/graphql",
        headers={
            "Api-Key": api_key,
            "Content-Type": "application/json",
        },
        json={
            "query": """
            query($accountId: Int!, $nrql: Nrql!) {
              actor {
                account(id: $accountId) {
                  nrql(query: $nrql) {
                    results
                  }
                }
              }
            }
            """,
            "variables": {
                "accountId": int(account_id),
                "nrql": nrql,
            },
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data["data"]["actor"]["account"]["nrql"]["results"]
