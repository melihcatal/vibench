from query_error_logs import query_error_logs

def incident_summary(time_range_minutes=60, config=None):
    config = config or {}
    error_logs_response = query_error_logs(time_range_minutes=time_range_minutes, config=config)
    error_logs = error_logs_response["logs"]

    if not error_logs:
        return {"summary": "No error logs found for the specified time range."}

    # In a real scenario, an LLM would summarize these logs.
    # For this example, we'll just concatenate the error messages.
    log_messages = [str(log["payload"]) for log in error_logs]
    
    # Placeholder for LLM summarization
    summary_text = "\n".join([f"Severity: {log['severity']}, Timestamp: {log['timestamp']}, Payload: {log['payload']}" for log in error_logs])

    return {"summary": f"Incident Summary (last {time_range_minutes} minutes):\n{summary_text}"}
