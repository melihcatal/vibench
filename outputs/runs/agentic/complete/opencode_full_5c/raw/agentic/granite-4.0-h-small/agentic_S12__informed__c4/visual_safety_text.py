import os
from tisane import TisaneClient
from typing import List, Dict


def check_generated_labels_for_unsafe_text(labels: List[str]) -> bool:
    """Run a text safety check on the list of extracted labels using Tisane.

    Args:
        labels: List of label strings produced by vision models.

    Returns:
        bool: True if all labels are safe, False otherwise.
    """
    client = TisaneClient()
    # Concatenate labels with newlines for moderation
    joined = "\n".join(labels)
    result = client.run(joined, language="en", targets=["profanity", "hate", "sex"])
    # Assume result['safe'] indicates overall safety (adjust per provider spec)
    return result.get("safe", True)
