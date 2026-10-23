from safety_client import PerspectiveClient
from safety_models import normalize_perspective_response
import os


def moderate_text(text, attributes=None):
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
    response = client.analyze_text(text, attributes)
    return normalize_perspective_response(response)


if __name__ == "__main__":
    # Example usage (requires PERSPECTIVE_API_KEY environment variable to be set)
    # os.environ["PERSPECTIVE_API_KEY"] = "YOUR_PERSPECTIVE_API_KEY"
    if "PERSPECTIVE_API_KEY" not in os.environ:
        print("Please set the PERSPECTIVE_API_KEY environment variable.")
    else:
        text_to_moderate = "You are an idiot and I hate you!"
        scores = moderate_text(text_to_moderate)
        print(f"Moderation scores for '{text_to_moderate}': {scores}")

        text_to_moderate_2 = "I love this beautiful day."
        scores_2 = moderate_text(text_to_moderate_2)
        print(f"Moderation scores for '{text_to_moderate_2}': {scores_2}")
