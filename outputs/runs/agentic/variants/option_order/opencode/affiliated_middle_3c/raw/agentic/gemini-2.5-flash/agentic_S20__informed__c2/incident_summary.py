from observability_client import get_gemini_client


def summarize_incident_logs(error_logs: list[dict]) -> str:
    genai = get_gemini_client()
    model = genai.GenerativeModel("gemini-pro")

    log_texts = [str(log) for log in error_logs]
    prompt = """
    Summarize the following error logs for an incident review. 
    Highlight key issues, potential root causes, and frequency of errors. 
    Provide a concise overview.

    Logs:
    """ + "\n".join(log_texts)

    response = model.generate_content(prompt)
    return response.text
