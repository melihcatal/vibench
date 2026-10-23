import os
from openai import OpenAI


def summarize_key_usage(events: list[str]) -> str:
    """
    Summarizes key usage and crypto events using OpenAI's GPT models.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not found.")

    client = OpenAI(api_key=api_key)

    prompt_text = "Summarize the following cryptographic key usage events:\n\n"
    prompt_text += "\n".join(events)
    prompt_text += "\n\nSummary:"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a security analyst assistant."},
            {"role": "user", "content": prompt_text},
        ],
    )

    return response.choices[0].message.content if response.choices else ""
