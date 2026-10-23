from observability_models import extract_messages


def summarize_incident(log_response: dict) -> dict:
    items = log_response.get("items", []) if isinstance(log_response, dict) else []
    messages = extract_messages(items)
    return {"error_count": len(items), "top_messages": messages[:5]}
