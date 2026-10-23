import os
import anthropic


def summarize_embedding_job(results):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    message = client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
        max_tokens=256,
        messages=[{"role": "user", "content": str(results)}],
    )
    return message.content[0].text

