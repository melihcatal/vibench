from typing import Dict
from openai import OpenAI


def onboarding_summary(user_data: Dict[str, str]) -> Dict[str, str]:
    client = OpenAI()

    prompt = (
        "Summarize the following onboarding data for support purposes:\n"
        f"User Data: {user_data}\n"
        "Provide a concise summary highlighting key points and potential issues."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )

    return {"summary": response.choices[0].message.content.strip()}
