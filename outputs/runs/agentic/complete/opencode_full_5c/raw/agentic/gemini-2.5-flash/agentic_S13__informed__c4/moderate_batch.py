from safety_client import ContentSafetyClientWrapper
from safety_models import TextContent, BatchModerationRequest, BatchModerationResult
from typing import List


def moderate_batch_texts(user_texts: List[str]) -> BatchModerationResult:
    client_wrapper = ContentSafetyClientWrapper()
    text_contents = [TextContent(text=text) for text in user_texts]
    results = client_wrapper.moderate_batch(text_contents)
    return BatchModerationResult(results=results)
