import os
from ibm_watsonx_ai.litellm import chat  # litellm wrapper for watsonx

# Load provider API credentials from env (one example)
watsonx_api_key = os.getenv("WATSONX_API_KEY")


def translate_invoice_notes(notes: str, target_lang: str = "en") -> str:
    """
    Translate extracted invoice notes/description to target language using Watsonx LLM.
    Returns translated text.
    """
    if not notes:
        return ""
    response = chat(
        model="granite",
        messages=[{"role": "user", "content": notes}],
        api_key=watsonx_api_key,
        target_lang=target_lang,
    )
    # Expected response format from litellm: {'choices': [{'message': {'content': '...'}}]}
    return (
        response["choices"][0]["message"]["content"]
        if response.get("choices")
        else notes
    )
