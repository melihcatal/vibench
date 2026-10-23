import os
from auth0.management import Auth0


def get_audit_summary():
    """
    Retrieves and summarizes audit events from Auth0.
    """
    auth0_domain = os.environ.get("AUTH0_DOMAIN")
    auth0_client_id = os.environ.get("AUTH0_MGMT_CLIENT_ID")
    auth0_client_secret = os.environ.get("AUTH0_MGMT_CLIENT_SECRET")

    auth0 = Auth0(auth0_domain, auth0_client_id, auth0_client_secret)

    # Get last 10 successful logins
    logs = auth0.logs.get_all(q="type:s", per_page=10, page=0, sort="date:-1")

    summary = {"total_logins": len(logs), "logins_by_user": {}}

    for log in logs:
        user_name = log.get("user_name", "unknown")
        if user_name not in summary["logins_by_user"]:
            summary["logins_by_user"][user_name] = 0
        summary["logins_by_user"][user_name] += 1

    return summary
