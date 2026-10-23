import requests


def claims_moderation(payload, config=None):
    text = payload.get("text", "")
    response = requests.post(
        "https://api.openai.com/v1/moderations",
        headers={"Authorization": f"Bearer {payload.get('api_key', '')}"},
        json={"model": "omni-moderation-latest", "input": text},
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()
    return {"flagged": result["results"][0]["flagged"], "result": result}
