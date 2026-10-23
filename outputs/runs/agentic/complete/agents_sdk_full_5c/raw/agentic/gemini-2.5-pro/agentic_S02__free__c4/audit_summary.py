import os
from datetime import datetime, timedelta
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client import ApiClient, Configuration

# Configuration for Datadog API
# Ensure DATADOG_API_KEY and DATADOG_APP_KEY are in your environment
configuration = Configuration()
api_client = ApiClient(configuration)
api_instance = LogsApi(api_client)

def get_login_summary(hours_ago: int = 24) -> dict:
    """
    Queries Datadog Logs for federated login events and returns a summary.
    """
    now = datetime.utcnow()
    start_time = now - timedelta(hours=hours_ago)
    
    query = "source:federated-login status:success"
    
    try:
        response = api_instance.list_logs(
            filter_query=query,
            filter_from=start_time.isoformat() + "Z",
            filter_to=now.isoformat() + "Z",
            page_limit=1000
        )
        
        logs = response.get('data', [])
        successful_logins = len(logs)
        
        # Example of further aggregation
        user_logins = {}
        for log in logs:
            user_id = log.get('attributes', {}).get('attributes', {}).get('user_id', 'unknown')
            user_logins[user_id] = user_logins.get(user_id, 0) + 1
            
        return {
            "summary_period_hours": hours_ago,
            "total_successful_logins": successful_logins,
            "unique_users": len(user_logins),
            "most_active_user": max(user_logins, key=user_logins.get) if user_logins else None
        }

    except Exception as e:
        print(f"Error querying Datadog logs: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    summary = get_login_summary(72)
    print(summary)
