import os
from openai import OpenAI
from query_error_logs import query_error_logs


def generate_incident_summary(
    service: str = None,
    time_window_hours: int = 1,
    max_errors: int = 50,
) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    from datetime import datetime, timezone, timedelta

    time_from = datetime.now(timezone.utc) - timedelta(hours=time_window_hours)

    query_result = query_error_logs(
        service=service,
        time_from=time_from,
        limit=max_errors,
    )

    if not query_result.entries:
        return "No error log entries found in the specified time window."

    error_lines = []
    for entry in query_result.entries[:max_errors]:
        error_lines.append(
            f"[{entry.timestamp}] status={entry.status} service={entry.service} "
            f"host={entry.host} message={entry.message}"
        )

    log_context = "\n".join(error_lines)

    prompt = (
        "You are an incident reviewer. Based on the following error log entries, "
        "provide a concise incident summary that includes:\n"
        "1. A brief overview of the incident\n"
        "2. The most likely root cause\n"
        "3. Affected services and hosts\n"
        "4. Recommended immediate actions\n\n"
        f"Error log entries:\n{log_context}\n\n"
        "Provide the summary in a structured format."
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are an experienced SRE who writes clear incident summaries.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=1024,
    )

    return response.choices[0].message.content
