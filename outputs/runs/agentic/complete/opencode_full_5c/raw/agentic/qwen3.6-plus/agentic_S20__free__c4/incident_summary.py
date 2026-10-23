import os
from datetime import datetime, timezone
from collections import Counter
from openai import OpenAI
from query_error_logs import query_error_logs
from observability_models import IncidentSummary


def generate_incident_summary(
    service: str = "*",
    severity: str = "error",
    hours_back: int = 24,
    limit: int = 100,
) -> IncidentSummary:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    error_response = query_error_logs(
        service=service,
        severity=severity,
        hours_back=hours_back,
        limit=limit,
    )

    entries = error_response.entries
    if not entries:
        return IncidentSummary(
            service=service,
            time_range=f"last {hours_back} hours",
            total_errors=0,
            error_categories={},
            affected_sources=[],
            top_messages=[],
            summary_text=f"No {severity} log entries found for service '{service}' in the last {hours_back} hours.",
            generated_at=datetime.now(timezone.utc).isoformat(),
        )

    error_categories = Counter()
    affected_sources = set()
    messages = []

    for entry in entries:
        error_categories[entry.level] += 1
        if entry.source:
            affected_sources.add(entry.source)
        messages.append(entry.message)

    message_counts = Counter(messages)
    top_messages = [msg for msg, _ in message_counts.most_common(5)]

    log_context = "\n".join(
        f"[{e.timestamp}] [{e.level}] ({e.source}) {e.message}" for e in entries[:20]
    )

    client = OpenAI(api_key=api_key)
    prompt = (
        f"Summarize the following error log findings for an incident review.\n\n"
        f"Service: {service}\n"
        f"Time range: last {hours_back} hours\n"
        f"Total errors: {len(entries)}\n"
        f"Error levels: {dict(error_categories)}\n"
        f"Affected sources: {', '.join(affected_sources)}\n\n"
        f"Recent log entries:\n{log_context}\n\n"
        f"Provide a concise incident summary in 2-3 sentences describing the likely root cause, "
        f"affected components, and recommended next steps."
    )

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are an incident response analyst. Summarize error logs concisely.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=300,
        temperature=0.3,
    )

    summary_text = completion.choices[0].message.content.strip()

    return IncidentSummary(
        service=service,
        time_range=f"last {hours_back} hours",
        total_errors=len(entries),
        error_categories=dict(error_categories),
        affected_sources=sorted(affected_sources),
        top_messages=top_messages,
        summary_text=summary_text,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )


if __name__ == "__main__":
    result = generate_incident_summary(
        service="payment-gateway",
        severity="error",
        hours_back=6,
    )
    print(result.model_dump_json(indent=2))
