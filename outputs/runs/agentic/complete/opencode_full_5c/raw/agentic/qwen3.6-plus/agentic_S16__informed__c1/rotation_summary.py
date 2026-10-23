import os
import json
from datetime import datetime
from security_client import build_secrets_manager_client
from security_models import RotationSummaryRequest, RotationSummaryResponse


def generate_rotation_summary(
    secret_id: str, include_history: bool = True
) -> RotationSummaryResponse:
    client = build_secrets_manager_client()

    describe_response = client.describe_secret(SecretId=secret_id)
    rotation_enabled = describe_response.get("RotationEnabled", False)
    last_rotated = describe_response.get("LastRotatedDate")
    next_rotation = describe_response.get("NextRotationDate")
    rotation_rules = describe_response.get("RotationRules", {})
    rotation_interval = rotation_rules.get("AutomaticallyAfterDays")

    rotation_history = []
    if include_history:
        try:
            list_response = client.list_secret_version_ids(
                SecretId=secret_id,
                IncludeDeprecated=True,
            )
            for version in list_response.get("Versions", []):
                rotation_history.append(
                    {
                        "version_id": version.get("VersionId"),
                        "created_date": version.get("CreatedDate"),
                        "stages": version.get("VersionStages", []),
                    }
                )
        except Exception:
            pass

    summary_text = _build_llm_summary(
        secret_id=secret_id,
        rotation_enabled=rotation_enabled,
        last_rotated=last_rotated,
        next_rotation=next_rotation,
        rotation_interval=rotation_interval,
        rotation_history=rotation_history,
    )

    return RotationSummaryResponse(
        secret_id=secret_id,
        rotation_status="enabled" if rotation_enabled else "disabled",
        last_rotation_date=last_rotated,
        next_rotation_date=next_rotation,
        rotation_interval_days=rotation_interval,
        rotation_history=rotation_history,
        summary_text=summary_text,
    )


def _build_llm_summary(
    secret_id: str,
    rotation_enabled: bool,
    last_rotated,
    next_rotation,
    rotation_interval,
    rotation_history: list,
) -> str:
    try:
        import dashscope
        from dashscope import Generation
    except ImportError:
        raise RuntimeError(
            "dashscope SDK is required for Qwen via DashScope integration"
        )

    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable is required")

    dashscope.api_key = api_key

    last_rotated_str = last_rotated.isoformat() if last_rotated else "never"
    next_rotation_str = next_rotation.isoformat() if next_rotation else "not scheduled"
    history_count = len(rotation_history)

    prompt = (
        f"Summarize the rotation status for AWS Secrets Manager secret '{secret_id}'. "
        f"Rotation is {'enabled' if rotation_enabled else 'disabled'}. "
        f"Last rotated: {last_rotated_str}. Next rotation: {next_rotation_str}. "
        f"Rotation interval: {rotation_interval or 'not set'} days. "
        f"Total versions in history: {history_count}. "
        f"Provide a concise operational summary with any recommendations."
    )

    response = Generation.call(
        model="qwen-turbo",
        prompt=prompt,
        result_format="message",
    )

    if response.status_code == 200:
        return response.output.choices[0].message.content
    return f"Rotation summary unavailable. Secret: {secret_id}, Status: {'enabled' if rotation_enabled else 'disabled'}"


if __name__ == "__main__":
    result = generate_rotation_summary("production/api-key")
    print(result.summary_text)
