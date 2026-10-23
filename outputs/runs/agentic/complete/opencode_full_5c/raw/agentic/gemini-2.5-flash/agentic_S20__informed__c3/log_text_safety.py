import requests
import os

# Perspective API documentation: https://developers.perspectiveapi.com/s/docs


def check_log_text_safety(log_message):
    """Checks selected log message text for unsafe content using the Perspective API.

    Args:
        log_message (str): The log message text to check for safety.

    Returns:
        dict: A dictionary containing safety scores or an error message.
    """
    perspective_api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not perspective_api_key:
        return {"error": "PERSPECTIVE_API_KEY environment variable not set."}

    api_url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={perspective_api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "comment": {"text": log_message},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()

        # Extract and simplify the scores
        summary_scores = {}
        for attr, data in result.get("attributeScores", {}).items():
            summary_scores[attr] = data.get("summaryScore", {}).get("value")

        return {"log_message": log_message, "safety_scores": summary_scores}

    except requests.exceptions.RequestException as e:
        return {"error": f"Perspective API request failed: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}


if __name__ == "__main__":
    # Example usage with different log messages
    messages_to_check = [
        "User 'bad_actor' attempted a SQL injection: SELECT * FROM users; DROP TABLE users;",
        "Application started successfully.",
        "This is a test message with some potentially harmful language.",
    ]

    print("\n--- Checking Log Text Safety ---")
    for msg in messages_to_check:
        safety_report = check_log_text_safety(msg)
        print(f"Log Message: '{msg}'")
        print(f"Safety Report: {safety_report}")
        print("---")
