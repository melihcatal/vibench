import os
import sys
import json
from datetime import datetime, timezone, timedelta

import dashscope
from dashscope import Generation

from observability_models import SlsClientConfig, IncidentFinding
from observability_client import (
    ObservabilityClient,
    build_error_query,
    build_time_range_query,
    extract_error_messages,
)


DASHSCOPE_MODEL = "qwen-turbo"


def summarize_error_logs(
    severity: str = "ERROR",
    hours_back: int = 1,
    service: str | None = None,
    max_results: int = 50,
) -> dict:
    dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY", "")

    config = SlsClientConfig.from_env()
    client = ObservabilityClient(config)

    from_time, to_time = build_time_range_query(
        from_time=datetime.now(timezone.utc) - timedelta(hours=hours_back),
        to_time=datetime.now(timezone.utc),
    )

    query = build_error_query(severity=severity)
    if service:
        query = f"{query} and service: {service}"

    result = client.get_logs(
        query=query,
        from_time=from_time,
        to_time=to_time,
        line=max_results,
        reverse=True,
    )

    error_logs = extract_error_messages(result)

    if not error_logs:
        return {
            "summary": "No error logs found in the specified time range.",
            "error_count": 0,
            "findings": [],
        }

    log_context = []
    for i, log in enumerate(error_logs[:20]):
        log_context.append(
            f"[{log.get('timestamp', 'unknown')}] [{log.get('severity', 'ERROR')}] "
            f"service={log.get('service', 'unknown')} "
            f"message={log.get('message', '')}"
        )

    prompt = (
        f"Analyze the following error logs from the past {hours_back} hour(s) and provide a concise incident summary. "
        f"Include: root cause hypothesis, affected services, error patterns, and recommended actions.\n\n"
        f"Error logs:\n" + "\n".join(log_context)
    )

    response = Generation.call(
        model=DASHSCOPE_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are an incident analysis assistant. Provide structured, actionable summaries of error logs.",
            },
            {"role": "user", "content": prompt},
        ],
        result_format="message",
    )

    summary_text = ""
    if response.status_code == 200:
        summary_text = response.output.choices[0].message.content
    else:
        summary_text = f"Error summarizing logs: {response.code} - {response.message}"

    findings = []
    for log in error_logs:
        finding = IncidentFinding(
            log_entry=log,
            severity=log.get("severity", "ERROR"),
            summary=summary_text,
        )
        findings.append(finding.to_dict())

    return {
        "summary": summary_text,
        "error_count": len(error_logs),
        "time_range": {
            "from": from_time.isoformat(),
            "to": to_time.isoformat(),
        },
        "findings": findings[:10],
    }


if __name__ == "__main__":
    severity = sys.argv[1] if len(sys.argv) > 1 else "ERROR"
    hours_back = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    result = summarize_error_logs(severity=severity, hours_back=hours_back)
    print(json.dumps(result, indent=2))
