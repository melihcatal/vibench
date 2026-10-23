from collections import Counter

from google.genai import Client

from query_error_logs import query_error_logs


def incident_summary(hours: int = 24) -> dict:
    errors = query_error_logs(hours=hours)
    client = Client()
    prompt = f"Summarize these log errors for incident review: {errors[:20]}"
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    severities = Counter(item.get("severity", "UNKNOWN") for item in errors)
    return {
        "summary": response.text,
        "severity_counts": dict(severities),
        "error_count": len(errors),
    }
