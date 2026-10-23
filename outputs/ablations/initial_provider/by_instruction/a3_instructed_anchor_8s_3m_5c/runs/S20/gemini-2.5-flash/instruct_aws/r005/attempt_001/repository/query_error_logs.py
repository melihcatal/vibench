import time
from typing import List, Dict, Any
from observability_client import ObservabilityClient
from observability_models import LogQueryResult

def query_error_logs(log_group_names: List[str], start_time_seconds: int, end_time_seconds: int, severity: str = "ERROR") -> LogQueryResult:
    client = ObservabilityClient()

    # CloudWatch Logs Insights query string
    query_string = f"fields @timestamp, @message | filter @message like /\"severity\":\"{{severity}}\"/ | sort @timestamp desc"
    query_string = query_string.replace(f'{{severity}}', severity)

    query_id = client.start_query(
        log_group_names=log_group_names,
        start_time=start_time_seconds,
        end_time=end_time_seconds,
        query_string=query_string
    )

    # Poll for query results (simplified for example, in real app might use a more robust polling mechanism)
    status = 'Running'
    while status in ['Running', 'Scheduled']:
        time.sleep(1) # Wait for 1 second before checking again
        results = client.get_query_results(query_id)
        status = results['status']

    if status == 'Complete':
        return LogQueryResult.from_aws_cloudwatch_insights_response(results)
    else:
        raise Exception(f"CloudWatch Logs Insights query failed with status: {status}")
