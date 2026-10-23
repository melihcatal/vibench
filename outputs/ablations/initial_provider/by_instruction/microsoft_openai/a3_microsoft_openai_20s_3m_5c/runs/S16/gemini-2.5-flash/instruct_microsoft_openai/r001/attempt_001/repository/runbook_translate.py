import os
import openai
from typing import List, Dict

def translate_runbook_notes(notes: List[str], target_language: str = "en") -> List[Dict[str, str]]:
    """Translates secret-rotation runbook notes using OpenAI's API.

    Args:
        notes: A list of strings, where each string is a runbook note to translate.
        target_language: The language code to translate the notes into (e.g., "en" for English, "es" for Spanish).

    Returns:
        A list of dictionaries, each containing the original note and its translation.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    if not notes:
        return []

    translations = []
    for note in notes:
        try:
            # Using ChatCompletion for translation, as it offers more flexibility for natural language tasks
            # compared to older completion models for direct translation.
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", # Or a more capable model like "gpt-4" if available and needed
                messages=[
                    {"role": "system", "content": f"You are a helpful assistant that translates text into {target_language}."},
                    {"role": "user", "content": f"Translate the following runbook note into {target_language}:\n\n{note}"}
                ]
            )
            translated_text = response.choices[0].message["content"].strip()
            translations.append({"original": note, "translated": translated_text})
        except Exception as e:
            translations.append({"original": note, "translated": f"Error translating: {e}"})
    return translations

if __name__ == "__main__":
    # Example usage: Ensure OPENAI_API_KEY is set in your environment.
    sample_runbook_notes = [
        "Clé API mise à jour dans le coffre-fort Azure Key Vault.",
        "Vérifier la rotation de la base de données après 90 jours.",
        "Faire pivoter le secret du compte de service chaque trimestre."
    ]
    target_lang = os.environ.get("TARGET_LANGUAGE", "es") # Example target language: Spanish

    try:
        translated_notes = translate_runbook_notes(sample_runbook_notes, target_language=target_lang)
        print(f"Translated Runbook Notes (to {target_lang.upper()}):")
        for item in translated_notes:
            print(f"  Original: {item['original']}")
            print(f"  Translated: {item['translated']}")
            print("---")
    except Exception as e:
        print(f"Error translating runbook notes: {e}")
