import os
import json
import requests
from typing import Dict


def moderate_claim(claim_text: str) -> Dict:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError("Azure Content Safety credentials are not configured.")

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {"Ocp-Apim-Subscription-Key": api_key, "Content-Type": "application/json"}

    payload = json.dumps(
        {
            "text": claim_text,
            "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
            "blocklistNames": [],
            "breakByBlocklists": True,
        }
    )

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {
            "error": str(e),
            "status_code": e.response.status_code if e.response else None,
        }


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    safe_text = "This is a user's biography."
    unsafe_text = (
        "This text contains hateful and violent content that should be flagged."
    )

    print("--- Moderating Safe Text ---")
    result_safe = moderate_claim(safe_text)
    print(json.dumps(result_safe, indent=2))

    print("\n--- Moderating Unsafe Text ---")
    result_unsafe = moderate_claim(unsafe_text)
    print(json.dumps(result_unsafe, indent=2))
