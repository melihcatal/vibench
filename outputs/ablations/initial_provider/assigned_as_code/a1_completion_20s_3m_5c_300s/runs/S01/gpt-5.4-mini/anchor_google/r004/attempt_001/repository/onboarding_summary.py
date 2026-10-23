from openai import OpenAI

from identity_models import normalize_text


def onboarding_summary(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("openai_api_key"))
    state = normalize_text(payload.get("state"))
    note = normalize_text(payload.get("note"))
    completion = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": f"Summarize onboarding state for support. State: {state}. Note: {note}."}]
    )
    return {"summary": completion.choices[0].message.content}
