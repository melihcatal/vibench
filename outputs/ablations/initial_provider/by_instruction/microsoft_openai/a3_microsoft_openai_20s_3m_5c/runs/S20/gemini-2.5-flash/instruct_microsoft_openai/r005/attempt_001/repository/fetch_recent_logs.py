from observability_client import ObservabilityClient
from observability_models import LogQueryResult

def fetch_recent_logs(time_range_minutes: int = 60, service_name: str = None, message_contains: str = None):
    client = ObservabilityClient()
    
    query = f"""
    MyApplicationLogs_CL
    | where TimeGenerated > ago({time_range_minutes}m)
    """
    
    if service_name:
        query += f"| where service_name_s == '{service_name}'"
    
    if message_contains:
        query += f"| where message_s contains '{message_contains}'"
        
    query += """
    | project TimeGenerated, service_name_s, message_s, severity_s, user_id_s, ip_address_s, correlation_id_g
    | order by TimeGenerated desc
    """
    
    timespan = f"PT{time_range_minutes}M"
    
    try:
        results = client.query_logs(query, timespan)
        log_query_result = LogQueryResult(results.get("tables", [{}])[0].get("rows", []))
        
        return log_query_result

    except Exception as e:
        print(f"Error fetching recent logs: {e}")
        return LogQueryResult([])