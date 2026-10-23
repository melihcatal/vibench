from safety_client import PerspectiveClient
from safety_models import normalize_perspective_response
import os


def moderate_batch(texts, attributes=None):
    if attributes is None:
        attributes = [
            "TOXICITY",
            "SEVERE_TOXICITY",
            "IDENTITY_ATTACK",
            "INSULT",
            "PROFANITY",
            "THREAT",
        ]

    client = PerspectiveClient()
    batch_decisions = []
    for text in texts:
        try:
            response = client.analyze_text(text, attributes)
            normalized_scores = normalize_perspective_response(response)
            batch_decisions.append({"text": text, "scores": normalized_scores})
        except Exception as e:
            batch_decisions.append({"text": text, "error": str(e)})
    return batch_decisions


if __name__ == "__main__":
    # Example usage (requires PERSPECTIVE_API_KEY environment variable to be set)
    # os.environ["PERSPECTIVE_API_KEY"] = "YOUR_PERSPECTIVE_API_KEY"
    if "PERSPECTIVE_API_KEY" not in os.environ:
        print("Please set the PERSPECTIVE_API_KEY environment variable.")
    else:
        messages = [
            "This is a wonderful day!",
            "You are so stupid, I hope you fail.",
            "I love programming.",
        ]
        decisions = moderate_batch(messages)
        for decision in decisions:
            print(
                f"Message: '{decision.get('text')}', Scores: {decision.get('scores')}, Error: {decision.get('error', 'None')}"
            )
