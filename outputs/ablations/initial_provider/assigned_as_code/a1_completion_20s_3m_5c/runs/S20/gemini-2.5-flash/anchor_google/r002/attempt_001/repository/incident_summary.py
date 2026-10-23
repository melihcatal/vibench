from observability_client import get_generative_model
from observability_models import IncidentSummaryRequest, IncidentSummaryResponse
from query_error_logs import query_error_logs
from observability_models import QueryLogRequest, LogEntry

def incident_summary(request: IncidentSummaryRequest) -> IncidentSummaryResponse:
    # Fetch error logs based on the provided query and time range
    # Assuming query_error_logs can handle time range in its filter_expression
    # For simplicity, let's construct a basic time filter
    import datetime
    end_time = datetime.datetime.now(datetime.timezone.utc)
    start_time = end_time - datetime.timedelta(hours=request.time_range_hours)

    time_filter = f"timestamp>=\"{start_time.isoformat()}\" AND timestamp<=\"{end_time.isoformat()}\""
    full_filter = f"{request.query} AND {time_filter}"

    log_query_request = QueryLogRequest(
        project_id=request.project_id,
        filter_expression=full_filter,
        order_by="timestamp desc"
    )
    error_logs_response = query_error_logs(log_query_request)
    error_entries = error_logs_response.entries

    if not error_entries:
        return IncidentSummaryResponse(
            summary="No error logs found for the given criteria.",
            error_count=0,
            log_entries=[]
        )

    # Prepare a prompt for the generative model
    log_messages = [f"Severity: {entry.severity}, Message: {entry.message}" for entry in error_entries]
    prompt = f"Summarize the following error logs for an incident review, identifying key issues and potential impact. Focus on common themes and unusual events.\n\nLogs:\n{"\n".join(log_messages)}"

    model = get_generative_model("gemini-pro")
    response = model.generate_content(prompt)
    summary_text = response.text

    return IncidentSummaryResponse(
        summary=summary_text,
        error_count=len(error_entries),
        log_entries=error_entries
    )
