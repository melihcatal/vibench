import os
from openai import OpenAI


def get_rotation_summary(rotation_log: str) -> str:
    """
    Generates a human-readable summary of a secret rotation log.
    """
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is not set in environment variables.")

    client = OpenAI()

    prompt = f"""
    The following is a log from a secret rotation event.
    Please provide a brief, one-sentence summary of the outcome.

    Log:
    {rotation_log}

    Summary:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful security assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=100,
            temperature=0.3,
        )
        if response.choices:
            return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"

    return "Could not generate summary."


if __name__ == "__main__":
    example_log = """
    INFO: Starting secret rotation for 'prod/db/credentials'.
    INFO: New secret version created with ID 'a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6'.
    INFO: Testing new secret with database 'prod-db-1.example.com'.
    SUCCESS: Database connection successful with new credentials.
    INFO: Updating 'AWSCURRENT' label to point to new version.
    SUCCESS: Secret rotation completed successfully.
    """
    summary = get_rotation_summary(example_log)
    print(summary)
