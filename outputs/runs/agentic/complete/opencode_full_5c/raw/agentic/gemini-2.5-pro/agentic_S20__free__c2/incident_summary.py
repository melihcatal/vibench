from observability_client import initialize_vertex_ai, get_gcp_project_id
from vertexai.generative_models import GenerativeModel


def summarize_errors_for_incident(error_logs: list[str]) -> str:
    initialize_vertex_ai()
    model = GenerativeModel("gemini-1.5-flash-001")

    log_text = "\n".join(error_logs)

    prompt = f"""
    The following are error logs from a recent incident. 
    Please summarize them into a brief incident report, highlighting the main error messages, 
    potential root cause, and impact.

    Logs:
    {log_text}
    """

    response = model.generate_content(prompt)
    return response.text


if __name__ == "__main__":
    sample_errors = [
        "ERROR:root:Database connection failed: timeout expired",
        "ERROR:root:Failed to process payment for user 'user123': Transaction declined",
        "ERROR:root:Database connection failed: timeout expired",
        "ERROR:root:API call to 'third-party-service' failed with status 503",
    ]
    summary = summarize_errors_for_incident(sample_errors)
    print("--- Incident Summary ---")
    print(summary)
