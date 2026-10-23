# appeal_translate.py

import os
from google.genai import GenerationOptions, GenerativeModel  # google-genai SDK (Gemini)
from google.auth import credentials

# Provider identifiers (make the provider identifiable in code)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def translate_appeal(appeal_text: str, target_lang: str = "en") -> str:
    """Translate appeal text using Gemini API (model: gemini-1.5-flash)."""
    model = GenerativeModel(model="gemini-1.5-flash")
    # Set minimal options for translation
    model.options = GenerationOptions(
        temperature=0.0,
        max_output_tokens=500,
    )
    # Simple prompt for translation
    messages = [
        {
            "role": "system",
            "content": "You are a translation model. Translate the following text to the target language.",
        },
        {
            "role": "user",
            "content": f"Translate from original language to {target_lang}:\\n\\n{appeal_text}",
        },
    ]
    response = model.generate_content(messages)
    return response.text.strip()


# Example usage (for local testing)
if __name__ == "__main__":
    sample = "Je ne suis pas d'accord avec la décision de blocage de mon compte."
    print("Translated:", translate_appeal(sample, target_lang="en"))
