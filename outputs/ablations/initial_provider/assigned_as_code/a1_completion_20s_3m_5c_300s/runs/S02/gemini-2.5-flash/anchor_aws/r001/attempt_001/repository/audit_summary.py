import os
from datetime import datetime, timedelta
from datadog_api_client.v1.api import logs_api
from datadog_api_client.v1.model import *
from datadog_api_client.v1.model.logs_list_request import LogsListRequest

def summarize_federated_login_audit_events(days_back=7):
    # Datadog API key and application key should be set as environment variables
    # DD_API_KEY, DD_APP_KEY
    configuration = logs_api.Configuration()

    with logs_api.LogsApi(logs_api.ApiClient(configuration)) as api_client:
        api = logs_api.LogsApi(api_client)
        now = datetime.utcnow()
        start_time = now - timedelta(days=days_back)

        query = "source:federated-login status:INFO"
        
        body = LogsListRequest(
            query=query,
            time={"from": start_time.isoformat(), "to": now.isoformat()},
            limit=1000  # Adjust limit as needed
        )

        try:
            response = api.list_logs(body=body)
            events = response.get('data', [])
            
            summary = {
                "total_events": len(events),
                "successful_logins": 0,
                "failed_logins": 0,
                "users": set(),
                "events": []
            }

            for event_data in events:
                event = event_data.get('content', {}).get('attributes', {})
                message = event.get('message', '')
                user_id = event.get('user.id')
                
                if "login_success" in message:
                    summary["successful_logins"] += 1
                elif "login_failure" in message:
                    summary["failed_logins"] += 1
                
                if user_id:
                    summary["users"].add(user_id)
                
                summary["events"].append({
                    "timestamp": event.get('timestamp'),
                    "message": message,
                    "user_id": user_id,
                    "status": event.get('status')
                })
            
            summary["unique_users"] = len(summary["users"])
            del summary["users"] # Remove set for JSON serialization

            return {"audit_summary": summary}
        except Exception as e:
            return {"error": str(e)}
