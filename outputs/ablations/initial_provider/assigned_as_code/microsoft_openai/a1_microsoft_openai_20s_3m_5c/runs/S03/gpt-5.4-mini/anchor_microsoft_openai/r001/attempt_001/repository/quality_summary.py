import os

import requests


def quality_summary(payload, config=None):
    config = config or {}
    api_key = config.get("api_key") or os.environ.get("OPENAI_API_KEY", "")
    response = requests.post(
        "https://api.openai.com/v1/responses",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": "gpt-5.4-mini",
            "input": f"Summarize translation quality issues for: {payload['text']}",
        },
        timeout=30,
    )
    response.raise_for_status()
    return {"summary": response.json()["output"][0]["content"][0]["text"]}
