import openai


def onboarding_summary(state: str):
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Summarize onboarding state for support."},
            {"role": "user", "content": state},
        ],
    )
    return {"summary": response.choices[0].message.content}
