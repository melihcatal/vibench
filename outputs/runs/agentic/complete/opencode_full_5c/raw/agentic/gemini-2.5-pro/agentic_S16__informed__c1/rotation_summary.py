import os
from openai import OpenAI
from security_models import SecretRotationStatus


def summarize_rotation_status(rotation_notes: str) -> SecretRotationStatus:
    """
    Summarizes secret rotation status using OpenAI's GPT model.
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
                    "content": "You are a helpful assistant that summarizes security events. Summarize the status of a secret rotation from the notes provided. Identify the secret ID and the final status (e.g., SUCCESS, FAILED, IN_PROGRESS).",
                },
                {"role": "user", "content": rotation_notes},
            ],
        )
        summary_text = response.choices[0].message.content

        # A simple parser to extract structured data from the summary
        lines = summary_text.split("\n")
        secret_id = "unknown"
        status = "unknown"
        for line in lines:
            if "Secret ID:" in line:
                secret_id = line.split("Secret ID:")[1].strip()
            if "Status:" in line:
                status = line.split("Status:")[1].strip()

        return SecretRotationStatus(
            secret_id=secret_id, status=status, summary=summary_text
        )
    except Exception as e:
        print(f"An error occurred while summarizing: {e}")
        return None


if __name__ == "__main__":
    notes = """
    Rotation for secret 'prod/db/master_password' initiated at 2023-10-27T10:00:00Z.
    Previous version moved to AWSPREVIOUS.
    New secret version created and tested against database instance.
    Application servers successfully restarted and using new secret.
    Rotation completed successfully at 2023-10-27T10:15:00Z.
    """
    summary = summarize_rotation_status(notes)
    if summary:
        print("Rotation Summary:")
        print(f"  Secret ID: {summary.secret_id}")
        print(f"  Status: {summary.status}")
        print(f"  Full Summary:\n{summary.summary}")
