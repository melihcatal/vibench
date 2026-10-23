import os
import google.generativeai as genai

# Configure Google Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def summarize_audit_events(audit_events: str) -> str:
    """
    Summarizes federated-login audit events using the Google Gemini API.
    Args:
        audit_events: A string containing a collection of audit event logs.
    Returns:
        A concise summary of the audit events.
    """
    if not GOOGLE_API_KEY:
        return "Error: GOOGLE_API_KEY not set."

    try:
        model = genai.GenerativeModel('gemini-pro') # Using 'gemini-pro' model
        prompt = f"Summarize the following federated login audit events, highlighting any anomalies or key trends:

{audit_events}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing audit events with Gemini API: {e}"

if __name__ == '__main__':
    # Example audit event data
    sample_audit_events = """
    [2023-10-27T10:00:00Z] user_id=user123 event_type=login provider=Auth0 status=success ip=192.168.1.100
    [2023-10-27T10:01:05Z] user_id=user456 event_type=login provider=Google status=success ip=192.168.1.101
    [2023-10-27T10:02:10Z] user_id=user123 event_type=login provider=Auth0 status=failure error="invalid_grant" ip=192.168.1.100
    [2023-10-27T10:03:15Z] user_id=user789 event_type=login provider=Auth0 status=success ip=172.16.0.50 (unusual IP)
    """
    summary = summarize_audit_events(sample_audit_events)
    print("Audit Summary:")
    print(summary)
