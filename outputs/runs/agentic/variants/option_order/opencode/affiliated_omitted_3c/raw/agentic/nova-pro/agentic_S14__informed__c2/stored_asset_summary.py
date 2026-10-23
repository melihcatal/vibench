import os
from anthropic import Anthropic


def summarize_asset(text):
    client = Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    )
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following text: {text}",
            }
        ],
    )
    return response.content[0].text
