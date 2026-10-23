import os
import anthropic


def summarize_onboarding_data(onboarding_data: str) -> str:
    client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )

    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following user onboarding state for a support ticket:\n\n{onboarding_data}",
            }
        ],
    )

    return message.content[0].text
