from observability_client import get_perspective_client


def check_log_safety(log_message: str) -> dict:
    """
    Checks a log message for unsafe content using the Perspective API.
    """
    client = get_perspective_client()

    analyze_request = {
        "comment": {"text": log_message},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
    }

    response = client.comments().analyze(body=analyze_request).execute()

    scores = {}
    for attribute, value in response["attributeScores"].items():
        scores[attribute] = value["summaryScore"]["value"]

    return scores


if __name__ == "__main__":
    message1 = "This is a normal log message about a user login."
    safety_scores1 = check_log_safety(message1)
    print(f"Safety scores for message 1: {safety_scores1}")

    message2 = "This log contains some really nasty and insulting user generated text."
    safety_scores2 = check_log_safety(message2)
    print(f"Safety scores for message 2: {safety_scores2}")
