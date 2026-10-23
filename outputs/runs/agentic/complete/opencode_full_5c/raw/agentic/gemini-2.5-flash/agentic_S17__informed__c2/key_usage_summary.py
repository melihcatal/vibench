import os
import google.generativeai as genai
from security_models import AuditLogEntry


def summarize_key_usage(audit_logs: list[AuditLogEntry]) -> str:
    """Summarizes key usage and crypto events using the Google Gemini API.

    Args:
        audit_logs: A list of AuditLogEntry objects representing crypto events.

    Returns:
        A string summary of the key usage and crypto events.
    """
    # Configure the Google Gemini API client
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # Prepare the prompt for the Gemini model
    log_strings = []
    for entry in audit_logs:
        log_strings.append(
            f"Timestamp: {entry.timestamp}, Event: {entry.event_type}, Key: {entry.key_id}, User: {entry.user}, Status: {entry.status}"
        )

    prompt = (
        "Summarize the following key management and cryptographic operation audit logs. "
        "Highlight any unusual activity, frequent key usage, or potential security concerns.\n\n"
        + "\n".join(log_strings)
    )

    try:
        # Use the Gemini Pro model for summarization
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        return response.text
    except Exception as e:
        raise RuntimeError(f"Error summarizing key usage with Google Gemini API: {e}")
