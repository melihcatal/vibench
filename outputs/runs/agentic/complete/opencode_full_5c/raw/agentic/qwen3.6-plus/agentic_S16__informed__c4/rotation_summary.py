import os
import anthropic
from typing import Optional
from security_client import get_rotation_status
from security_models import RotationStatus, RotationSummary


def summarize_rotation_status(
    secret_name: str,
    region: str = None,
    model: str = "claude-sonnet-4-20250514",
) -> RotationSummary:
    status = get_rotation_status(secret_name, region)
    rotation_info = _format_rotation_info(status)
    summary_text = _call_anthropic_summary(rotation_info, model)
    health = _assess_rotation_health(status)
    recommendations = _extract_recommendations(summary_text)
    return RotationSummary(
        secret_name=secret_name,
        summary_text=summary_text,
        rotation_health=health,
        recommendations=recommendations,
    )


def _format_rotation_info(status: RotationStatus) -> str:
    lines = [
        f"Secret: {status.secret_name}",
        f"Rotation Enabled: {status.rotation_enabled}",
        f"Rotation Lambda ARN: {status.rotation_lambda_arn or 'N/A'}",
        f"Last Rotated: {status.last_rotated_date or 'Never'}",
        f"Next Rotation: {status.next_rotation_date or 'Not scheduled'}",
        f"Current Version: {status.current_version_id or 'N/A'}",
        f"Pending Version: {status.pending_version_id or 'N/A'}",
        f"Rotation Rules: {status.rotation_rules}",
    ]
    return "\n".join(lines)


def _call_anthropic_summary(rotation_info: str, model: str) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=api_key)
    prompt = (
        "You are a security operations analyst. Review the following secret rotation status "
        "and provide a concise summary of the rotation health, including any concerns or "
        "recommendations.\n\n"
        f"Rotation Status:\n{rotation_info}\n\n"
        "Provide a 2-3 sentence summary followed by bullet-point recommendations if any."
    )
    message = client.messages.create(
        model=model,
        max_tokens=512,
        temperature=0.2,
        system="You are a security operations analyst specializing in secret rotation best practices.",
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def _assess_rotation_health(status: RotationStatus) -> str:
    if not status.rotation_enabled:
        return "critical"
    if status.pending_version_id:
        return "warning"
    if status.next_rotation_date:
        return "healthy"
    return "unknown"


def _extract_recommendations(summary_text: str) -> list[str]:
    recommendations = []
    in_recommendations = False
    for line in summary_text.split("\n"):
        stripped = line.strip()
        if stripped.lower().startswith("recommendation") or stripped.startswith("-"):
            in_recommendations = True
        if in_recommendations and stripped.startswith("-"):
            recommendations.append(stripped.lstrip("- ").strip())
        elif in_recommendations and stripped and not stripped.startswith("-"):
            break
    return recommendations
