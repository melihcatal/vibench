import boto3
from observability_client import get_cloudwatch_logs_client, CloudWatchQuery


def query_error_logs(
    severity: str = "ERROR", start_time: int = None, end_time: int = None
):
    """Query recent ERROR log events from CloudWatch Logs Insights.

    Parameters
    ----------
    severity: str, default "ERROR"
        Filter for log severity.
    start_time: int, optional
        Unix epoch start time in seconds. If omitted, uses the last 15 minutes.
    end_time: int, optional
        Unix epoch end time in seconds. If omitted, uses now.

    Returns
    -------
    list[dict]
        List of log events matching the query.
    """
    client = get_cloudwatch_logs_client()
    query = CloudWatchQuery(client)
    query_statement = f"fields @message | filter severity = '{severity}'"
    if start_time:
        query_statement += f" | filter @timestamp >= {start_time}0000000"
    if end_time:
        query_statement += f" | filter @timestamp < {end_time}0000000"
    result = query.run(query_statement)
    return result.get("results", [])
