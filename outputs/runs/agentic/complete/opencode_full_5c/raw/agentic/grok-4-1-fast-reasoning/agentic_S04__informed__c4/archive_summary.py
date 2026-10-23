import os
import anthropic


def archive_summary(
    transcript_text: str,
    model: str = "claude-3-5-sonnet-20240620",
    max_tokens: int = 1000,
) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is required")
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=0.1,
        messages=[
            {
                "role": "user",
                "content": f"Provide a concise summary of this meeting transcript:\\n\\n{transcript_text}",
            }
        ],
    )
    return message.content[0].text
