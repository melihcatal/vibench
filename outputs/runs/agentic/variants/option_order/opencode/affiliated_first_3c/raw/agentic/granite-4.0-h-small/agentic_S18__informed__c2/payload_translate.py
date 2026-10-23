import json
from typing import Dict, Any, Optional
from ibm_watsonx_ai.translate import TranslationClient
from messaging_client import get_client


def translate_payload(
    payload: Dict[str, Any], target_lang: str = "es", *, preserve_keys: bool = True
) -> Dict[str, Any]:
    """Translate customer‑facing text fields inside a payload to a target language.

    Uses the watsonx.ai Translation service (same-scenario provider) with
    credentials from WATSONX_API_KEY and WATSONX_PROJECT_ID. Only string
    fields whose key ends with '_text' or '_description' are translated;
    other fields are preserved. The original text is kept under a _src suffix
    for audit purposes.

    Parameters:
        payload (dict): Original JSON payload.
        target_lang (str): ISO language code (default "es" for Spanish).
        preserve_keys (bool): If True, keep original fields; otherwise replace.
    Returns:
        dict: New payload dict with translated texts.
    """
    # Extract text fields to translate
    translation_tasks: List[Dict[str, Any]] = []
    for key, value in payload.items():
        if isinstance(value, str):
            if key.endswith("_text") or key.endswith("_description"):
                # Preserve original under _src suffix
                payload[f"{key}_src"] = value
                translation_tasks.append({"source": value, "target_lang": target_lang})
    if not translation_tasks:
        # Nothing to translate
        return payload
    # Initialize translation client (uses same credentials as guardrails)
    translator = TranslationClient()
    # Send batch request (the client supports up to 25 items)
    translations = translator.translate_batch(
        sources=[t["source"] for t in translation_tasks], target_lang=target_lang
    )
    # Map translated results back to payload
    for src_key, tr in zip([t["source"] for t in translation_tasks], translations):
        # Derive the original key (remove _src suffix)
        if preserve_keys:
            original_key = src_key.replace("_src", "")
        else:
            original_key = src_key
        # Overwrite or add the translated version
        payload[original_key] = tr
    return payload


# Example usage (for local testing)
if __name__ == "__main__":
    sample = {
        "event_id": "test-123",
        "type": "order_created",
        "timestamp": "2025-08-15T12:34:56Z",
        "customer_name_text": "Welcome, Alice!",
        "order_summary_description": "Your order with 3 items will ship tomorrow.",
    }
    translated = translate_payload(sample, target_lang="fr")
    print("Original:", json.dumps(sample, indent=2))
    print("Translated:", json.dumps(translated, indent=2))
