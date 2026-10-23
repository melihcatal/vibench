import os
import openai
from typing import Dict, Any
from security_models import SecretRotationSummary

def summarize_rotation_status(rotation_data: Dict[str, Any]) -> SecretRotationSummary:
    """Summarizes secret rotation status using OpenAI GPT model."""
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    # Example of rotation_data:
    # {"secret_id": "my-db-secret", "last_rotation_log": "Secret rotated successfully on 2023-10-26. Next rotation due 2024-01-26.", "current_status_report": "Secret is active and healthy. No issues detected.", "rotation_policy": "Rotate every 90 days.", "latest_version_creation_date": "2023-10-26"}

    prompt = f"""
    Analyze the following secret rotation data and provide a concise summary, including last rotation date, next rotation due date if available, and an overall status (Healthy, Overdue, Warning). Also, provide brief notes. Ensure the output is structured to easily create a SecretRotationSummary object.

    Secret ID: {rotation_data.get("secret_id", "N/A")}
    Last Rotation Log: {rotation_data.get("last_rotation_log", "N/A")}
    Current Status Report: {rotation_data.get("current_status_report", "N/A")}
    Rotation Policy: {rotation_data.get("rotation_policy", "N/A")}
    Latest Version Creation Date: {rotation_data.get("latest_version_creation_date", "N/A")}

    Summary Format:
    Secret ID: <id>
    Last Rotated: <date>
    Next Rotation Due: <date>
    Status: <status>
    Notes: <notes>
    """

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Using a concrete model identifier
        messages=[
            {"role": "system", "content": "You are a helpful assistant for summarizing secret rotation status."},
            {"role": "user", "content": prompt}
        ]
    )

    summary_text = response.choices[0].message.content.strip()

    # Parse the summary_text into SecretRotationSummary
    summary_lines = summary_text.split('\n')
    summary_dict = {}
    for line in summary_lines:
        if ': ' in line:
            key, value = line.split(': ', 1)
            summary_dict[key.strip()] = value.strip()

    return SecretRotationSummary(
        secret_id=summary_dict.get("Secret ID", rotation_data.get("secret_id", "Unknown")),
        last_rotated=summary_dict.get("Last Rotated"),
        next_rotation_due=summary_dict.get("Next Rotation Due"),
        status=summary_dict.get("Status", "Unknown"),
        notes=summary_dict.get("Notes"),
    )

if __name__ == "__main__":
    # Example usage
    sample_rotation_data = {
        "secret_id": "my-app-db-password",
        "last_rotation_log": "Secret was automatically rotated on 2023-11-01 03:00 UTC. Previous version retired. Next rotation scheduled for 2024-02-01.",
        "current_status_report": "All services using this secret are reporting successful connections. Monitoring shows normal usage patterns.",
        "rotation_policy": "Automated rotation every 92 days. Alerts triggered 7 days before due date if rotation fails.",
        "latest_version_creation_date": "2023-11-01"
    }

    try:
        summary = summarize_rotation_status(sample_rotation_data)
        print(f"\nSecret Rotation Summary for {summary.secret_id}:")
        print(f"  Last Rotated: {summary.last_rotated}")
        print(f"  Next Rotation Due: {summary.next_rotation_due}")
        print(f"  Status: {summary.status}")
        print(f"  Notes: {summary.notes}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
