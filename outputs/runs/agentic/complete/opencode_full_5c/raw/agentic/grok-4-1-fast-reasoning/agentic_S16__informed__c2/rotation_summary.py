import anthropic
import os


def summarize_rotation_status(rotation_notes: str) -> str:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=500,
        temperature=0.7,
        messages=[
            {
                "role": "user",
                "content": f"Summarize the secret rotation status based on these notes:\\n\\n{rotation_notes}",
            }
        ],
    )
    return message.content[0].text
