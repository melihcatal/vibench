from typing import List
from ibm_watsonx_ai import WatsonxApi


def check_unsafe_content(log_texts: List[str], threshold: float = 0.8) -> List[bool]:
    """Check selected log message text for unsafe content using watsonx guardrails.

    Returns a list of booleans corresponding to each log text, True indicates safe.
    Required environment variables:
        WATSONX_API_KEY
        WATSONX_PROJECT_ID
    """
    client = WatsonxApi(text_moderation=True)
    # Batch the texts; API supports up to 100 per request
    safe_flags = []
    for i in range(0, len(log_texts), 100):
        batch = log_texts[i : i + 100]
        resp = client.post(
            f"/v1/text_moderation", json={"texts": batch, "model": "watsonx-moderation"}
        )
        resp.raise_for_status()
        results = resp.json()
        safe_flags.extend(
            [result["safe"] >= threshold for result in results["results"]]
        )
    return safe_flags
