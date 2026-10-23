import os
from openai import OpenAI


def onboarding_summary(state_json: str) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "system", "content": "Summarize onboarding state for support."}, {"role": "user", "content": state_json}])
    return response.choices[0].message.content or ""
