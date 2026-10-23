import os
import requests

def check_content_safety(text):
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    url = f"{endpoint}/contentsafety/text:analyze"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }

    body = {
        "text": text,
        "categories": ["Hate", "Sexual", "SelfHarm", "Violence"],
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    result = response.json()

    return {
        "is_safe": all(
            result["categoriesAnalysis"][category]["severity"] < 4
            for category in body["categories"]
        ),
        "details": result,
    }