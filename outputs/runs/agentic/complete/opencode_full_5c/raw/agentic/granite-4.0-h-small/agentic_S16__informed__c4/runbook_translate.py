import json
from google.genai import (
    GenerationConfig,
    GenerativeModel,
)  # using Anthropic (Claude) as concrete provider


def translate_runbook(note: str, target_lang: str = "es") -> str:
    """Translate secret rotation runbook notes to a target language using a hosted LLM.

    Uses Anthropic Claude as the concrete provider.  Returns the translated text.

    Args:
        note (str): Original runbook commentary (usually English).
        target_lang (str): ISO language code for desired output.

    Returns:
        str: Translated note.
    """
    model = GenerativeModel("claude-3-5-sonnet-20240620")
    generation_config = GenerationConfig(temperature=0.0, generation_type="chat")
    # Prompt the model to translate
    response = model.generate_content(
        f"Translate the following English runbook note into {target_lang}:",
        content=note,
        generation_config=generation_config,
    )
    # The model returns a string directly
    return response.content[0].text


# Quick demo (only runs when file executed directly)
if __name__ == "__main__":
    english_note = (
        "Rotate secret v2 after breach investigation; update monitoring alerts."
    )
    print(translate_runbook(english_note, "fr"))
