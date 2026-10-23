import requests


def claims_moderation(payload, config=None):
    response = requests.post(
        "https://api.openai.com/v1/moderations",
        headers={"Authorization": f"Bearer {(config or {}).get('api_key')}"},
        json={"model": "omni-moderation-latest", "input": payload.get("text", "")},
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()["results"][0]
    return {"flagged": result["flagged"], "categories": result["categories"], "category_scores": result["category_scores"]}
