"""
Moderates user-provided text claims (e.g., a profile bio or username)
for toxicity using the Perspective API.
"""
import os
import requests
from typing import Optional

def moderate_claim(text: str) -> Optional[float]:
    """
    Analyzes a string for toxicity using the Perspective API.

    Args:
        text: The text string to analyze.

    Returns:
        The toxicity score (0.0 to 1.0), or None if an error occurs.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # The Perspective API is a Google API, but it's not part of GCP
    # and has its own endpoint and key management.
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    payload = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}}
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        toxicity_score = data['attributeScores']['TOXICITY']['summaryScore']['value']
        return toxicity_score
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return None
    except (KeyError, TypeError) as e:
        print(f"Error parsing Perspective API response: {e}")
        return None

# Example usage:
# if __name__ == '__main__':
#     user_bio_safe = "I am a software developer who loves hiking and open-source."
#     user_bio_toxic = "I hate everyone and everything."

#     score_safe = moderate_claim(user_bio_safe)
#     if score_safe is not None:
#         print(f"Toxicity score for safe bio: {score_safe:.4f}")

#     score_toxic = moderate_claim(user_bio_toxic)
#     if score_toxic is not None:
#         print(f"Toxicity score for toxic bio: {score_toxic:.4f}")
