import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def summarize_error_log_findings(error_log: str, incident_context: Optional[str] = None) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = [
        {
            "role": "system",
            "content": "You summarize error-log findings for incident review. Return concise, structured output."
        },
        {
            "role": "user",
            "content": (
                "Summarize the key error-log findings for incident review. "
                "Include likely impact, suspected root cause, notable error patterns, and immediate follow-up actions.\n\n"
                f"Incident context: {incident_context or 'N/A'}\n\n"
                f"Error log:\n{error_log}"
            ),
        },
    ]
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=prompt,
        temperature=0.2,
    )
    summary = response.choices[0].message.content or ""
    return {
        "provider": "openai",
        "model": "gpt-5.4-mini",
        "summary": summary.strip(),
    }


def build_incident_summary(error_log: str, incident_context: Optional[str] = None) -> str:
    result = summarize_error_log_findings(error_log, incident_context)
    return result["summary"]
