import os
from datetime import datetime
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem


def summarize_login_to_datadog(user_id: str, ip_address: str, success: bool):
    """
    Sends a structured log summary of a login event to Datadog.

    Requires DATADOG_API_KEY and DATADOG_SITE environment variables.
    """
    if not os.environ.get("DATADOG_API_KEY"):
        raise ValueError("DATADOG_API_KEY is not set.")

    configuration = Configuration()
    with ApiClient(configuration) as api_client:
        api_instance = LogsApi(api_client)
        
        log_item = HTTPLogItem(
            ddsource="python-federated-login",
            ddtags=f"env:prod,login_status:{'success' if success else 'failure'}",
            hostname=os.environ.get("HOSTNAME", "unknown"),
            service="auth-service",
            message=f"Login attempt for user {user_id} {'succeeded' if success else 'failed'}",
            attributes={
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "ip_address": ip_address,
                "login_successful": success,
                "provider": "federated",
            },
        )
        
        body = HTTPLog([log_item])

        try:
            api_response = api_instance.submit_log(body)
            print("Successfully sent log to Datadog.")
            return api_response
        except Exception as e:
            print(f"Error sending log to Datadog: {e}")
            raise
