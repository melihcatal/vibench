import os
import requests


def summarize_records(records):
    api_key = os.getenv("MISTRAL_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"prompt": "Summarize the following records:", "records": records}
    response = requests.post(
        "https://api.mistral.ai/v1/summarize", headers=headers, json=data
    )
    return response.json()["summary"]
