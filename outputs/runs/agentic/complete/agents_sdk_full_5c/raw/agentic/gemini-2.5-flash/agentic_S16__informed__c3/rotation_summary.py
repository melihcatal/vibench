import anthropic
import os

def summarize_rotation_status(rotation_logs: str) -> str:
    """
    Summarizes secret rotation status using the Anthropic Messages API.
    """
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    model_name = "claude-3-opus-20240229" # Using a concrete model identifier

    try:
        response = client.messages.create(
            model=model_name,
            max_tokens=500,
            messages=[
                {"role": "user", "content": f"Summarize the following secret rotation logs, highlighting successes, failures, and any critical issues:

{rotation_logs}"}
            ]
        )
        return response.content[0].text
    except Exception as e:
        print(f"Error summarizing rotation status with Anthropic API: {e}")
        raise

