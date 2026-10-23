# [LATER-STEP] translate_transcript.py
# Translate completed transcript segments using Azure AI Translator SDK

import os
import azure.ai.translation.translate as translator

AZURE_TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY")
AZURE_TRANSLATOR_REGION = os.getenv("AZURE_TRANSLATOR_REGION", "global")

if not AZURE_TRANSLATOR_KEY:
    raise RuntimeError("AZURE_TRANSLATOR_KEY environment variable not set")


def translate_transcript(transcript: str, target_language: str = "es") -> str:
    """Translates the provided transcript text to the target language using Azure Translator.
    Returns the translated transcript.
    """
    client = translator.TranslatorClient(endpoint=f"https://{AZURE_TRANSLATOR_REGION}.translator.cognitive.microsoft.com/",
                                          credential=translator.AzureKeyCredential(AZURE_TRANSLATOR_KEY))
    # Azure Translator translates a single string; split transcript into sentences for batch handling
    sentences = [s.strip() for s in transcript.split('.') if s.strip()]
    translations = []
    for sent in sentences:
        response = client.translate(content=sent, target_language=target_language, source_language="en")
        # response.translations[0].text holds the translated text
        translations.append(response.translations[0].text)
    return " ".join(translations)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: translate_transcript.py <transcript_text> [target_language]")
        sys.exit(1)
    transcript = sys.argv[1]
    target = sys.argv[2] if len(sys.argv) > 2 else "es"
    translated = translate_transcript(transcript, target)
    print("Translated transcript:")
    print(translated)
