# corpus_safety.py
# [LATER-STEP] Check corpus text for safety before embedding

import os
from embeddings_client import get_watsonx_client
from ibm_watsonx_ai.services import ContentSafety

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

cs_client = ContentSafety(client=get_watsonx_client())


def is_corpus_safe(text: str) -> bool:
    """Check if a corpus text is safe according to WatsonX guardrails."""
    result = cs_client.check_content(text=text, type="text")
    # Assume the API returns a boolean flag in result['safe']
    return result.get("safe", False)
