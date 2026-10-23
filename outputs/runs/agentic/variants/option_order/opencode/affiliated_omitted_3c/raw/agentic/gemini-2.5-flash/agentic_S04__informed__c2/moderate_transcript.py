import os
import requests
import json


def moderate_text(text: str) -> dict:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    payload = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
        "outputType": "FourSeverityLevels",
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during content moderation: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    # Example usage
    text_to_moderate_safe = "This is a perfectly safe and innocent sentence."
    moderation_result_safe = moderate_text(text_to_moderate_safe)
    print(f"Moderation Result (Safe):\n{json.dumps(moderation_result_safe, indent=2)}")

    # Example with potentially unsafe content (adjust as needed for testing)
    text_to_moderate_unsafe = "I hate you all! You are terrible."
    moderation_result_unsafe = moderate_text(text_to_moderate_unsafe)
    print(
        f"Moderation Result (Unsafe):\n{json.dumps(moderation_result_unsafe, indent=2)}"
    )
