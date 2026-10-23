from observability_client import ObservabilityClient
import google.generativeai as genai


def incident_summary(error_logs: list[dict]) -> str:
    client = ObservabilityClient()
    model = genai.GenerativeModel(client.gemini_model)

    if not error_logs:
        return "No error logs provided for summary."

    log_texts = [log.get("message", "") for log in error_logs]
    prompt = (
        "Summarize the following error logs to identify potential incidents. "
        "Focus on common patterns, severity, and potential root causes:\n\n"
        + "\n".join(log_texts)
    )

    response = model.generate_content(prompt)
    return response.text
