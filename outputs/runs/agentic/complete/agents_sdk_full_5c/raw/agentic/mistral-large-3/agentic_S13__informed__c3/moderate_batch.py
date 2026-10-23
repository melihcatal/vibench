from typing import List
from concurrent.futures import ThreadPoolExecutor
from safety_client import get_watsonx_client
from safety_models import TextModerationResponse


def moderate_batch(texts: List[str], max_workers: int = 4) -> List[TextModerationResponse]:
    """
    Moderate a batch of texts using WatsonX.ai guardrails.
    Returns list of normalized moderation responses.
    """
    client = get_watsonx_client()

    def _moderate_single(text: str) -> TextModerationResponse:
        raw_response = client.analyze_text(text)
        return TextModerationResponse.from_watsonx(raw_response)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(_moderate_single, texts))

    return results