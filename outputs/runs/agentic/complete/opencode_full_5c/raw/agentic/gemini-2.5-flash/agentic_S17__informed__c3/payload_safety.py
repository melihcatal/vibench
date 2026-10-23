import requests
import os


def check_payload_safety(text_payload: str) -> dict:
    """
    Checks decrypted text payloads for unsafe content using Perspective API.
    """
    perspective_api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not perspective_api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={perspective_api_key}"

    headers = {"Content-Type": "application/json"}

    data = {
        "comment": {"text": text_payload},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # Raise an exception for HTTP errors

    return response.json()


if __name__ == "__main__":
    # Example usage with a sample decrypted payload
    decrypted_text = "I hate you, you are the worst!"

    try:
        safety_check_results = check_payload_safety(decrypted_text)
        print("Payload Safety Check Results (Perspective API):")

        for attribute, scores in safety_check_results.get(
            "attributeScores", {}
        ).items():
            print(f"- {attribute}: {scores['summaryScore']['value']:.2f}")
            if scores["summaryScore"]["value"] > 0.5:  # Example threshold
                print(f"  WARNING: High {attribute} score detected.")

    except Exception as e:
        print(f"Error checking payload safety: {e}")
