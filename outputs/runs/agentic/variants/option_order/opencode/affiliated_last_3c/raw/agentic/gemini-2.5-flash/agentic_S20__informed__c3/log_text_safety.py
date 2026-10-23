import os
import requests


def check_log_text_safety(log_message: str) -> dict:
    # PERSPECTIVE_API_KEY environment variable should be set
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        return {"error": "PERSPECTIVE_API_KEY environment variable not set."}

    # The Perspective API endpoint
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    # Construct the request body
    request_body = {
        "comment": {"text": log_message},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
        },
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=request_body, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        analysis_results = response.json()

        # Extract scores for common attributes
        scores = {}
        for attr, data in analysis_results.get("attributeScores", {}).items():
            scores[attr] = data.get("summaryScore", {}).get("value", 0.0)

        return {"log_message": log_message, "safety_scores": scores}
    except requests.exceptions.RequestException as e:
        return {"error": f"Error checking text safety with Perspective API: {e}"}


if __name__ == "__main__":
    # Example usage
    message1 = "This is a perfectly normal log message."
    message2 = "You are an idiot! This system is terrible and slow."
    message3 = "I will hack into your system and destroy everything!"

    safety_report1 = check_log_text_safety(message1)
    safety_report2 = check_log_text_safety(message2)
    safety_report3 = check_log_text_safety(message3)

    print("\n--- Safety Report 1 ---")
    print(safety_report1)

    print("\n--- Safety Report 2 ---")
    print(safety_report2)

    print("\n--- Safety Report 3 ---")
    print(safety_report3)
