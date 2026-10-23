from openai import OpenAI


def onboarding_summary(state_text: str):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Summarize this onboarding state for support:\n{state_text}",
            }
        ],
    )
    return response.choices[0].message.content
