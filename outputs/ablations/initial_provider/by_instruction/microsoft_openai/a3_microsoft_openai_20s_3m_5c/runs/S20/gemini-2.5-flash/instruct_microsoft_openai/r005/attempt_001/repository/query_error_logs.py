from observability_client import ObservabilityClient
from observability_models import LogQueryResult

def query_error_logs(time_range_minutes: int = 60):
    client = ObservabilityClient()
    
    query = f"""
    MyApplicationLogs_CL
    | where severity_s == 'Error'
    | where TimeGenerated > ago({time_range_minutes}m)
    | project TimeGenerated, service_name_s, message_s, severity_s, error_code_s
    | order by TimeGenerated desc
    """
    
    timespan = f"PT{time_range_minutes}M"
    
    try:
        results = client.query_logs(query, timespan)
        log_query_result = LogQueryResult(results.get("tables", [{}])[0].get("rows", []))
        
        return log_query_result

    except Exception as e:
        print(f"Error querying error logs: {e}")
        return LogQueryResult([])