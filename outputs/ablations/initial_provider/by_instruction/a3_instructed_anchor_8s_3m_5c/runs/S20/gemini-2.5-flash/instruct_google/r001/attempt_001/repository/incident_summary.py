import google.generativeai as genai
import os
from observability_models import LogEntry, IncidentSummaryRequest, IncidentSummaryResponse

def summarize_error_logs(request: IncidentSummaryRequest) -> IncidentSummaryResponse:
    """
    Summarizes error log findings for incident review using Google Gemini Pro.

    Args:
        request: An IncidentSummaryRequest object containing error logs and optional context.

    Returns:
        An IncidentSummaryResponse object with the summary, recommendations, and key findings.
    """
    # Configure the API key. Ensure GOOGLE_API_KEY is set in your environment variables.
    # For production, consider more secure ways to manage API keys.
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    log_texts = []
    for log in request.error_logs:
        log_entry_str = f"Timestamp: {log.timestamp}, Severity: {log.severity}, LogName: {log.log_name}, Resource: {log.resource_type}"
        if log.json_payload:
            log_entry_str += f", Payload: {log.json_payload}"
        elif log.text_payload:
            log_entry_str += f", Message: {log.text_payload}"
        log_texts.append(log_entry_str)
    
    all_logs_text = "\n".join(log_texts)

    prompt = """
    Analyze the following error logs to provide a concise incident summary, key findings, and actionable recommendations.

    Error Logs:
    {}

    Context: {}

    Please provide:
    1. A brief summary of the incident.
    2. Key findings (e.g., common errors, affected services, timeframes).
    3. Recommendations for investigation and resolution.
    """.format(all_logs_text, request.context if request.context else "None provided.")

    response = model.generate_content(prompt)
    
    summary_text = response.text
    
    # Attempt to parse summary into structured format (this is a simplified example)
    # In a real scenario, you might use a more robust parsing or instruct the model to output JSON.
    summary = "No summary generated."
    key_findings = []
    recommendations = []

    lines = summary_text.split('\n')
    current_section = ""
    for line in lines:
        if "1. summary" in line.lower() or "summary of the incident" in line.lower():
            current_section = "summary"
        elif "2. key findings" in line.lower() or "key findings:" in line.lower():
            current_section = "key_findings"
        elif "3. recommendations" in line.lower() or "recommendations for investigation" in line.lower():
            current_section = "recommendations"
        elif line.strip():
            if current_section == "summary":
                summary = line.strip()
            elif current_section == "key_findings":
                key_findings.append(line.strip())
            elif current_section == "recommendations":
                recommendations.append(line.strip())

    return IncidentSummaryResponse(summary=summary, key_findings=key_findings, recommendations=recommendations)

if __name__ == "__main__":
    # Example usage (replace with actual log entries)
    sample_error_logs = [
        LogEntry(
            timestamp="2026-09-19T10:00:00Z",
            severity="ERROR",
            log_name="my-app-logs",
            resource_type="cloud_run_revision",
            json_payload={"error_code": "DB-CONN-001", "message": "Database connection failed"},
            labels={'env': 'prod'}
        ),
        LogEntry(
            timestamp="2026-09-19T10:01:30Z",
            severity="ERROR",
            log_name="my-app-logs",
            resource_type="cloud_run_revision",
            text_payload="Unhandled exception in user service: NullPointerException",
            labels={'env': 'prod'}
        ),
        LogEntry(
            timestamp="2026-09-19T10:05:00Z",
            severity="ERROR",
            log_name="auth-service-logs",
            resource_type="cloud_function",
            json_payload={"error_code": "AUTH-005", "message": "Invalid JWT token"},
            labels={'env': 'prod'}
        ),
    ]

    request = IncidentSummaryRequest(
        error_logs=sample_error_logs,
        context="Investigating a spike in application errors during peak hours."
    )

    # Ensure GOOGLE_API_KEY environment variable is set for this example to run
    # os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY"

    try:
        summary_response = summarize_error_logs(request)
        print("\n--- Incident Summary ---")
        print(f"Summary: {summary_response.summary}")
        print("Key Findings:")
        for finding in summary_response.key_findings:
            print(f"  - {finding}")
        print("Recommendations:")
        for recommendation in summary_response.recommendations:
            print(f"  - {recommendation}")
    except Exception as e:
        print(f"Error summarizing logs: {e}")
        print("Please ensure GOOGLE_API_KEY environment variable is set and valid.")
