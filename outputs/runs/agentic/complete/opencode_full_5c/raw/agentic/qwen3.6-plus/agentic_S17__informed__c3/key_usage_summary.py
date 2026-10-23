import os
import json
import logging
from typing import Optional, List, Dict

from mistralai import Mistral

from security_models import KeyUsageEvent, KeyUsageSummary

logger = logging.getLogger(__name__)

MISTRAL_SERVICE = "Mistral Chat API"
MISTRAL_MODEL = "mistral-large-latest"
MISTRAL_API_KEY_ENV = "MISTRAL_API_KEY"


def build_events_context(events: List[KeyUsageEvent]) -> str:
    lines = []
    for event in events:
        status = "SUCCESS" if event.success else "FAILED"
        line = (
            f"- [{event.timestamp}] {event.operation} on key {event.key_id}: {status}"
        )
        if event.algorithm:
            line += f" (algorithm: {event.algorithm})"
        if event.error_message:
            line += f" Error: {event.error_message}"
        lines.append(line)
    return "\n".join(lines)


def summarize_key_usage(
    key_id: str,
    events: List[KeyUsageEvent],
    api_key: Optional[str] = None,
    model: str = MISTRAL_MODEL,
) -> KeyUsageSummary:
    total = len(events)
    successful = sum(1 for e in events if e.success)
    failed = total - successful

    breakdown: Dict[str, int] = {}
    for event in events:
        breakdown[event.operation] = breakdown.get(event.operation, 0) + 1

    events_text = build_events_context(events)

    prompt = (
        f"You are a security analyst summarizing AWS KMS key usage for key ID: {key_id}.\n\n"
        f"Key usage events:\n{events_text}\n\n"
        f"Total operations: {total}\n"
        f"Successful: {successful}\n"
        f"Failed: {failed}\n"
        f"Operations breakdown: {json.dumps(breakdown)}\n\n"
        f"Provide a concise 3-4 sentence summary of the key usage patterns, "
        f"highlighting any anomalies, failures, or notable trends. "
        f"Focus on security implications and operational health."
    )

    client = Mistral(api_key=api_key or os.environ[MISTRAL_API_KEY_ENV])

    response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a security operations analyst specializing in cloud key management.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.3,
        max_tokens=500,
    )

    summary_text = response.choices[0].message.content.strip()

    logger.info(
        "Generated key usage summary for %s using %s model %s",
        key_id,
        MISTRAL_SERVICE,
        model,
    )

    return KeyUsageSummary(
        key_id=key_id,
        total_operations=total,
        successful_operations=successful,
        failed_operations=failed,
        operations_breakdown=breakdown,
        recent_events=events[-10:],
        summary_text=summary_text,
    )


def summarize_multiple_keys(
    key_events: Dict[str, List[KeyUsageEvent]],
    api_key: Optional[str] = None,
    model: str = MISTRAL_MODEL,
) -> Dict[str, KeyUsageSummary]:
    results = {}
    for key_id, events in key_events.items():
        results[key_id] = summarize_key_usage(
            key_id=key_id,
            events=events,
            api_key=api_key,
            model=model,
        )
    return results
