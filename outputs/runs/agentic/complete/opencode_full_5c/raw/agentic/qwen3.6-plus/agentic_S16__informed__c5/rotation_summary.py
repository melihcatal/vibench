import os
from typing import Optional
from openai import OpenAI
from security_models import RotationStatus, format_rotation_summary
from security_client import fetch_rotation_status


def summarize_rotation_status(
    secret_id: str,
    region: str = None,
    model: str = "gpt-4o",
    api_key: str = None,
) -> str:
    status = fetch_rotation_status(secret_id, region)
    summary_text = format_rotation_summary(status)
    prompt = (
        f"Analyze the following AWS Secrets Manager rotation status report "
        f"and provide a concise summary with any recommendations:\n\n"
        f"{summary_text}\n\n"
        f"Provide: (1) current rotation health assessment, "
        f"(2) any issues or concerns, "
        f"(3) recommended actions."
    )
    client = OpenAI(api_key=api_key or os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a security operations assistant specializing in secret rotation analysis.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=500,
    )
    return response.choices[0].message.content


def summarize_rotation_from_status(
    status: RotationStatus,
    model: str = "gpt-4o",
    api_key: str = None,
) -> str:
    summary_text = format_rotation_summary(status)
    prompt = (
        f"Analyze the following secret rotation status and provide a concise summary:\n\n"
        f"{summary_text}\n\n"
        f"Provide: (1) current rotation health, (2) issues, (3) recommendations."
    )
    client = OpenAI(api_key=api_key or os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a security operations assistant specializing in secret rotation analysis.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=500,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    secret_id = os.environ.get("ROTATION_SECRET_ID", "prod/database/postgres-primary")
    result = summarize_rotation_status(secret_id)
    print(result)
