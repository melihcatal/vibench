import os
import google.generativeai as genai
from observability_client import configure_gemini_client
from observability_models import SummarizationRequest

def summarize_incident_logs(summary_request: SummarizationRequest) -> str:
    """
    Summarizes error-log findings for incident review using the Google Gemini API.
    """
    try:
        configure_gemini_client()
    except ValueError as e:
        return f"Error configuring Gemini client: {e}"

    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""
    Please summarize the following log data for an incident review.
    Focus on key events, potential causes, impacted components, and any immediate actions suggested by the logs.
    
    Summary Length: {summary_request.summary_length}
    Target Audience: {summary_request.target_audience}

    Log Data:
    '''
    {summary_request.log_data}
    '''

    Provide a concise summary.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary with Gemini API: {e}"

if __name__ == "__main__":
    # Example log data (you would typically fetch this from query_error_logs.py)
    example_log_data = """
    2023-10-27T10:00:01Z [ERROR] service=auth-api, message="Authentication failed for user 'jdoe': Invalid credentials", user_id="jdoe", ip_address="192.168.1.10"
    2023-10-27T10:00:05Z [WARNING] service=auth-api, message="High rate of failed login attempts from IP 192.168.1.10", threshold=10, current=15
    2023-10-27T10:00:10Z [ERROR] service=order-processor, message="Database connection refused", db_host="prod-db-01", port=5432
    2023-10-27T10:00:11Z [CRITICAL] service=order-processor, message="Fatal error: Could not connect to primary database. Switching to fallback.", db_host="prod-db-01"
    2023-10-27T10:00:15Z [INFO] service=monitoring, message="Alert fired: Primary database connection lost for order-processor."
    2023-10-27T10:00:20Z [ERROR] service=auth-api, message="Rate limiting activated for IP 192.168.1.10"
    """

    print("--- Generating short incident summary ---")
    short_summary_req = SummarizationRequest(
        log_data=example_log_data,
        summary_length="short",
        target_audience="DevOps Engineer"
    )
    short_summary = summarize_incident_logs(short_summary_req)
    print(short_summary)

    print("\n--- Generating detailed incident summary ---")
    detailed_summary_req = SummarizationRequest(
        log_data=example_log_data,
        summary_length="detailed",
        target_audience="Security Analyst"
    )
    detailed_summary = summarize_incident_logs(detailed_summary_req)
    print(detailed_summary)
