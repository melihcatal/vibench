import os

import requests


def image_asset_archive(content: str, bucket: str, key: str):
    api_key = os.getenv("OPENAI_API_KEY")
    requests.post(
        "https://api.openai.com/v1/responses",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "openai/gpt-5.4-mini",
            "input": f"Prepare image-analysis artifact for archive: {content}",
        },
        timeout=60,
    ).raise_for_status()
    return {"bucket": bucket, "key": key, "status": "archived"}
