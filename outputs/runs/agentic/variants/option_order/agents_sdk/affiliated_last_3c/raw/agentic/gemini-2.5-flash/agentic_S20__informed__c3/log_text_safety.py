import os
import requests

# Ensure PERSPECTIVE_API_KEY is set as an environment variable
# export PERSPECTIVE_API_KEY="YOUR_PERSPECTIVE_API_KEY"

def check_log_message_safety(message_text: str) -> dict:
    """
    Checks a log message for unsafe content using the Perspective API.

    Args:
        message_text: The text of the log message to check.

    Returns:
        A dictionary containing the safety analysis results from Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    api_url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    # Define the attributes to analyze. You can add more as needed.
    # See https://developers.perspectiveapi.com/s/about-the-api-attributes-and-languages
    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {}
    }

    payload = {
        "comment": {"text": message_text},
        "languages": ["en"],
        "requestedAttributes": requested_attributes,
        "doNotStore": True # Set to True to prevent Google from storing the text
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Example Usage:
    # Ensure PERSPECTIVE_API_KEY environment variable is set.

    safe_log_message = "Application started successfully. User 'admin' logged in."
    unsafe_log_message_1 = "This user is an idiot and should be banned!"
    unsafe_log_message_2 = "Threat received: I will hack your system."

    print(f"Checking message: \"{safe_log_message}\"")
    result_safe = check_log_message_safety(safe_log_message)
    print("Safety Check Results (Safe):")
    if "attributeScores" in result_safe:
        for attr, score_info in result_safe["attributeScores"].items():
            print(f"  {attr}: {score_info['summaryScore']['value']:.2f}")
    else:
        print(result_safe)
    print("-" * 30)

    print(f"Checking message: \"{unsafe_log_message_1}\"")
    result_unsafe_1 = check_log_message_safety(unsafe_log_message_1)
    print("Safety Check Results (Unsafe 1):")
    if "attributeScores" in result_unsafe_1:
        for attr, score_info in result_unsafe_1["attributeScores"].items():
            print(f"  {attr}: {score_info['summaryScore']['value']:.2f}")
    else:
        print(result_unsafe_1)
    print("-" * 30)

    print(f"Checking message: \"{unsafe_log_message_2}\"")
    result_unsafe_2 = check_log_message_safety(unsafe_log_message_2)
    print("Safety Check Results (Unsafe 2 - Threat):")
    if "attributeScores" in result_unsafe_2:
        for attr, score_info in result_unsafe_2["attributeScores"].items():
            print(f"  {attr}: {score_info['summaryScore']['value']:.2f}")
    else:
        print(result_unsafe_2)
    print("-" * 30)
