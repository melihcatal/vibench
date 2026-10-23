from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor
from moderate_text import moderate_text


def moderate_batch(
    messages: List[str], category_thresholds: Dict[str, str] = None
) -> List[Dict[str, Any]]:
    """
    Moderates a batch of user messages using Google Cloud's Content Moderation API.
    Returns per-message decisions with scores and attribute details.
    """
    results = []

    def process_message(message: str) -> Dict[str, Any]:
        return moderate_text(message, category_thresholds)

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(process_message, messages))

    return results
