import os
from typing import List, Dict
from moderate_text import moderate_text
from safety_models import ContentSafetyResponse

def moderate_batch(texts: List[str]) -> Dict[str, ContentSafetyResponse]:
    """Moderates a batch of user messages and returns per-message decisions using Azure AI Content Safety."""
    batch_results = {}
    for i, text in enumerate(texts):
        try:
            result = moderate_text(text)
            batch_results[f"message_{i}"] = result
        except Exception as e:
            print(f"Error moderating text '{text}': {e}")
            # Optionally, you can return a default error response or re-raise
            batch_results[f"message_{i}"] = ContentSafetyResponse(error=str(e))
    return batch_results

if __name__ == "__main__":
    # Example usage (requires environment variables AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY)
    # os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"] = "YOUR_ENDPOINT"
    # os.environ["AZURE_CONTENT_SAFETY_KEY"] = "YOUR_KEY"
    # test_batch = [
    #     "This is a perfectly safe message.",
    #     "I hate you so much!",
    #     "Let's discuss adult topics."
    # ]
    # results = moderate_batch(test_batch)
    # for msg_id, res in results.items():
    #     print(f"{msg_id}: {res.to_dict()}")
    pass
