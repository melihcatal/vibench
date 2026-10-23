# appeal_translate.py
# LATER-STEP implementation
# Translate appeal text for human reviewer

from ibm_watsonx_ai import IbmWatsonXAIClient

client = IbmWatsonXAIClient(output_format="json")
MODEL_ID = "watsonx.guardrails:1.0.0"


def translate_appeal(text: str, target_lang: str = "en") -> str:
    """Translate user appeal into English using watsonx guardrails model family.

    Returns the translated string.
    """
    response = client.translator.translate(
        text=text, target_language=target_lang, model_id=MODEL_ID
    )
    # response format varies; assume it contains 'translated_text'
    return response.get("translated_text", "")


# Example usage (not executed)
# appeal = client_input.get('appeal')
# english_appeal = translate_appeal(appeal)
