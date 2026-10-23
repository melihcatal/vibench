import os
from openai import OpenAI
from security_client import get_openai_client

def translate_compliance_note(note_text: str, target_language: str = "English") -> str:
    """
    Translates encryption or compliance notes for reviewers using OpenAI's chat completion API.
    """
    client = get_openai_client()

    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Using a concrete model identifier
            messages=[
                {"role": "system", "content": f"You are a professional translator. Translate the following compliance or encryption note into {target_language}."},
                {"role": "user", "content": note_text}
            ]
        )
        translated_text = response.choices[0].message.content
        return translated_text
    except Exception as e:
        return f"Translation failed: {e}"

if __name__ == '__main__':
    example_note_french = "La clé de chiffrement a été renouvelée conformément à la politique de sécurité."
    translated_note_english = translate_compliance_note(example_note_french, "English")
    print(f"Original (French): {example_note_french}")
    print(f"Translated (English): {translated_note_english}\n")

    example_note_german = "Die Verschlüsselungsrichtlinie wurde aktualisiert, um neue Vorschriften zu erfüllen."
    translated_note_spanish = translate_compliance_note(example_note_german, "Spanish")
    print(f"Original (German): {example_note_german}")
    print(f"Translated (Spanish): {translated_note_spanish}")
