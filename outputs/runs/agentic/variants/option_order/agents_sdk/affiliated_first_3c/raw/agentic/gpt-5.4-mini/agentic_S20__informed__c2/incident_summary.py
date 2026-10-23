from observability_models import QueryResult, summarize_messages
from observability_client import load_config
from query_error_logs import query_error_logs


def incident_summary(minutes: int = 60) -> str:
    load_config()
    result: QueryResult = query_error_logs(minutes=minutes)
    count = len(result.entries)
    sample = summarize_messages(result.entries)
    return f"Datadog incident review: {count} error log entries in the last {minutes} minutes. Sample: {sample}"
