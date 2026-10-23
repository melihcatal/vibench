import os
from openai import OpenAI

def summarize_onboarding_state(onboarding_data: str) -> str:
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    client = OpenAI(api_key=openai_api_key)

    # Using OpenAI's chat completions API for summarization
    # Model ID: gpt-3.5-turbo
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes onboarding status."},
            {"role": "user", "content": f"Summarize the following onboarding state for support: {onboarding_data}"}
        ]
    )

    return response.choices[0].message.content
