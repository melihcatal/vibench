import os
from openai import OpenAI


def summarize_rotation_status(status_text: str) -> str:
    """
    Summarizes the secret rotation status using the OpenAI API.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a security analyst assistant. Summarize the following secret rotation status logs concisely for a security report.",
                },
                {"role": "user", "content": status_text},
            ],
            temperature=0.3,
            max_tokens=150,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "No summary generated."
    except Exception as e:
        return f"Error generating summary: {e}"


if __name__ == "__main__":
    log_data = """
    - 2023-10-26 10:00:00Z: Rotation started for secret 'prod/db/main'. Version ID: abc-123.
    - 2023-10-26 10:00:05Z: Successfully created new secret version. Version ID: def-456.
    - 2023-10-26 10:00:10Z: Updated database credentials for user 'webapp'.
    - 2023-10-26 10:00:15Z: Application health checks passing with new secret.
    - 2023-10-26 10:00:20Z: Marked new version 'def-456' as AWSCURRENT.
    - 2023-10-26 10:00:25Z: Old version 'abc-123' is now AWSPREVIOUS. Rotation successful.
    """
    summary_report = summarize_rotation_status(log_data)
    print("--- Rotation Status Summary ---")
    print(summary_report)
