import os
import json
import requests

OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_CHAT_URL = "https://api.openai.com/v1/chat/completions"
ONBOARDING_SUMMARY_MODEL = "gpt-4o-mini"


def onboarding_summary(onboarding_state):
    api_key = os.environ[OPENAI_API_KEY_ENV]

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    state_json = json.dumps(onboarding_state, indent=2)

    system_prompt = (
        "You are a support assistant. Summarize the onboarding state of a user "
        "into a concise, structured summary for a support agent. "
        "Include account status, completed steps, pending actions, and any issues."
    )

    payload = {
        "model": ONBOARDING_SUMMARY_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Onboarding state:\n{state_json}"},
        ],
        "temperature": 0.3,
        "max_tokens": 500,
    }

    response = requests.post(OPENAI_CHAT_URL, json=payload, headers=headers, timeout=60)
    response.raise_for_status()

    result = response.json()
    summary_text = result["choices"][0]["message"]["content"]

    return {
        "summary": summary_text,
        "model_used": ONBOARDING_SUMMARY_MODEL,
        "usage": result.get("usage", {}),
    }
