from observability_client import get_vertex_ai_model
from typing import List

def summarize_error_logs_for_incident(log_messages: List[str]) -> str:
    model = get_vertex_ai_model("gemini-pro")

    prompt = (
        "Summarize the following error log messages into a concise incident report. "
        "Highlight key issues, potential root causes, and frequency of errors.\n\n"
        "Log Messages:\n" + "\n".join([f"- {msg}" for msg in log_messages]) + "\n\n"
        "Incident Summary:"
    )

    response = model.generate_content(
        prompt,
        generation_config={"temperature": 0.2}
    )
    
    return response.candidates[0].content.parts[0].text