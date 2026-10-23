import os
import openai


def summarize_rotation_event(status_text: str) -> str:
    """
    Summarizes secret rotation status notes using OpenAI GPT.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = openai.OpenAI(api_key=api_key)

    try:
        prompt = f"Summarize the following secret rotation status into a single, concise sentence:\n\n{status_text}"
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant for security operations.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=100,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate summary."
    except Exception as e:
        print(f"An error occurred with the OpenAI API: {e}")
        return "Summary generation failed."


if __name__ == "__main__":
    rotation_status = (
        "Rotation process initiated for secret 'prod/db/creds'. "
        "Successfully created a new secret version. "
        "Pending validation in the staging environment. "
        "Current secret version remains AWSCURRENT. "
        "New version marked as AWSPENDING."
    )
    summary = summarize_rotation_event(rotation_status)
    print("Rotation Status Summary:")
    print(summary)
