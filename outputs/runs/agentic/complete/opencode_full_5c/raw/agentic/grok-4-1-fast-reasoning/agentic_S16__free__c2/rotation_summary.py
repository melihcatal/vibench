import os
import json
from security_client import get_secrets_client
from openai import OpenAI


def summarize_rotation_status(secret_name: str) -> str:
    client = get_secrets_client()
    desc_resp = client.describe_secret(SecretId=secret_name)
    status_info = {
        "rotation_enabled": desc_resp.get("RotationEnabled"),
        "rotation_lambda_arn": desc_resp.get("RotationLambdaARN"),
        "rotation_rules": desc_resp.get("RotationRules"),
        "last_rotated_date": desc_resp.get("LastRotatedDate"),
        "last_changed_date": desc_resp.get("LastChangedDate"),
        "created_date": desc_resp.get("CreatedDate"),
    }
    status_str = json.dumps(status_info, default=str, indent=2)
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize secret rotation status concisely and clearly.",
            },
            {
                "role": "user",
                "content": f"Summarize this AWS Secrets Manager rotation status:\n{status_str}",
            },
        ],
        max_tokens=150,
    )
    return response.choices[0].message.content
