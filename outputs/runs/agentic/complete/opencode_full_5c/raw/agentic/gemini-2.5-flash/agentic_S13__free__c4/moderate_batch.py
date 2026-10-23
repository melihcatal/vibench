import os
from typing import List, Dict
from google.cloud import language_v2  # Provider identifiable import
from moderate_text import moderate_text_content


def moderate_batch_content(texts: List[str], project_id: str) -> List[Dict]:
    """Moderates a batch of user messages and returns per-message decisions.

    Args:
        texts: A list of texts to moderate.
        project_id: The Google Cloud project ID.

    Returns:
        A list of dictionaries, where each dictionary contains moderation scores for a text.
    """
    batch_results = []
    for text in texts:
        scores = moderate_text_content(text, project_id)
        batch_results.append({"text": text, "scores": scores})
    return batch_results


if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    if project_id == "your-gcp-project-id":
        print(
            "Please set the GOOGLE_CLOUD_PROJECT environment variable or replace 'your-gcp-project-id' with your actual project ID."
        )
    else:
        texts_to_moderate = [
            "I love this product! It's amazing.",
            "You are an idiot. I hate you.",
            "Let's meet tomorrow at 3 PM.",
            "Kill yourself!",
        ]
        results = moderate_batch_content(texts_to_moderate, project_id)
        for result in results:
            print(f"Text: '{result['text']}'\n  Scores: {result['scores']}\n")
