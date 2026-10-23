import os
import json
from typing import List
from security_models import RotationStatus
from security_client import get_aws_client, handle_aws_error
import dashscope
from dashscope import Generation


DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")
dashscope.api_key = DASHSCOPE_API_KEY


def get_rotation_status(secret_name: str, region: str = None) -> RotationStatus:
    client = get_aws_client(region)
    try:
        response = client.describe_secret(SecretId=secret_name)
        rotation_rules = response.get("RotationRules", {})
        version_ids_to_stages = response.get("VersionIdsToStages", {})
        current_version = None
        staged_version = None
        for vid, stages in version_ids_to_stages.items():
            if "AWSCURRENT" in stages:
                current_version = vid
            if "AWSPENDING" in stages:
                staged_version = vid
        return RotationStatus(
            secret_name=secret_name,
            rotation_enabled=response.get("RotationEnabled", False),
            last_rotated_date=response.get("LastRotatedDate", "").isoformat()
            if response.get("LastRotatedDate")
            else None,
            next_rotation_date=None,
            rotation_lambda_arn=response.get("RotationLambdaARN"),
            current_version_id=current_version or "",
            staged_version_id=staged_version,
            provider="AWS Secrets Manager",
        )
    except Exception as e:
        raise handle_aws_error(e, secret_name)


def summarize_rotation_status(rotation_status: RotationStatus) -> str:
    status_text = json.dumps(rotation_status.to_dict(), indent=2)
    prompt = (
        f"Analyze the following AWS Secrets Manager rotation status and provide a concise summary "
        f"of the rotation health, any pending rotations, and recommendations:\n\n{status_text}"
    )
    response = Generation.call(
        model="qwen-turbo",
        prompt=prompt,
        max_tokens=500,
        temperature=0.3,
    )
    if response.status_code == 200:
        return response.output.text
    else:
        raise RuntimeError(
            f"DashScope Qwen API error: {response.code} - {response.message}"
        )


def summarize_multiple_secrets(secret_names: List[str], region: str = None) -> dict:
    results = {}
    for name in secret_names:
        status = get_rotation_status(name, region)
        summary = summarize_rotation_status(status)
        results[name] = {
            "status": status.to_dict(),
            "summary": summary,
        }
    return results


if __name__ == "__main__":
    secret_name = os.environ.get("AWS_SECRET_NAME", "production/api-key")
    status = get_rotation_status(secret_name)
    summary = summarize_rotation_status(status)
    print(json.dumps({"status": status.to_dict(), "summary": summary}, indent=2))
