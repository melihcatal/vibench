from googleapiclient import discovery
import os
from typing import List

def moderate_batch(texts: List[str]) -> List[dict]:
    """
    Moderates a batch of user messages and returns per-message decisions using Perspective API.
    Note: Perspective API does not have a native batch endpoint, so we simulate it with individual calls.
    For true batching, consider Google Cloud Content Safety API if available for your region and use case.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    results = []
    for text in texts:
        analyze_request = {
            'comment': {'text': text},
            'requestedAttributes': {
                'TOXICITY': {},
                'SEVERE_TOXICITY': {},
                'IDENTITY_ATTACK': {},
                'INSULT': {},
                'PROFANITY': {},
                'THREAT': {}
            }
        }
        response = client.comments().analyze(body=analyze_request).execute()
        results.append(response)
    return results

if __name__ == '__main__':
    # Example usage:
    # Ensure PERSPECTIVE_API_KEY is set in your environment
    # messages = [
    #     "You are an idiot!",
    #     "Hello, how are you doing today?",
    #     "I will hurt you."
    # ]
    # batch_results = moderate_batch(messages)
    # for i, res in enumerate(batch_results):
    # print(f"Message {i+1}: {res}")
    pass
