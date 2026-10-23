import os
import json
from security_client import get_openai_client
from security_models import SecretRotationSummary


def summarize_rotation_status(
    secret_name: str, secret_data: dict
) -> SecretRotationSummary:
    client = get_openai_client()
    prompt = f"Summarize the secret rotation status for the secret named '{secret_name}' based on the following data: {secret_data}. Provide a 'last_rotated' date, 'next_rotation_due' date, and a brief 'summary_text'. If dates are not explicit, infer them or state they are not available. Use YYYY-MM-DD format for dates. If date is not available, use 'N/A'. The output should be a JSON object with keys: last_rotated, next_rotation_due, summary_text."

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes secret rotation information.",
                },
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
        )
        summary_json = response.choices[0].message.content
        summary_dict = json.loads(summary_json)

        return SecretRotationSummary(
            secret_name=secret_name,
            last_rotated=summary_dict.get("last_rotated", "N/A"),
            next_rotation_due=summary_dict.get("next_rotation_due", "N/A"),
            summary_text=summary_dict.get("summary_text", "No summary available."),
        )
    except Exception as e:
        return SecretRotationSummary(
            secret_name=secret_name,
            last_rotated="Error",
            next_rotation_due="Error",
            summary_text=f"Failed to summarize rotation status: {e}",
        )

        summary_json = response.choices[0].message.content
        summary_dict = eval(summary_json)  # Using eval for parsing JSON-like string

        return SecretRotationSummary(
            secret_name=secret_name,
            last_rotated=summary_dict.get("last_rotated", "N/A"),
            next_rotation_due=summary_dict.get("next_rotation_due", "N/A"),
            summary_text=summary_dict.get("summary_text", "No summary available."),
        )
    except Exception as e:
        return SecretRotationSummary(
            secret_name=secret_name,
            last_rotated="Error",
            next_rotation_due="Error",
            summary_text=f"Failed to summarize rotation status: {e}",
        )
