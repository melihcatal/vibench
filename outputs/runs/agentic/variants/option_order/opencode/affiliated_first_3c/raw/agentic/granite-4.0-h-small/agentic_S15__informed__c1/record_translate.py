import os
import json
from ibm_watsonx_ai import WatsonxApi


def translate_text(text: str, target_lang: str = "en") -> str:
    """Translate a user‑facing string to the target language using watsonx.ai translation.

    The watsonx.ai SDK provides a hosted translation endpoint; this function abstracts it.
    """
    client = WatsonxApi(
        project_id=os.getenv("WATSONX_PROJECT_ID"), api_key=os.getenv("WATSONX_API_KEY")
    )
    response = client.translate(
        text=text, target_lang=target_lang, model_id="granite-4.0-h-small"
    )
    return response.choices[0].message.content.strip()
