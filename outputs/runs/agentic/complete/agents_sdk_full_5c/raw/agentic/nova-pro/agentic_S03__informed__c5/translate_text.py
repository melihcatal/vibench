import os
from azure.ai.translation.text import TextTranslationClient, TextTranslationInput

client = TextTranslationClient(endpoint=f"https://{os.getenv('AZURE_TRANSLATOR_REGION')}.api.cognitive.microsoft.com", credential=os.getenv('AZURE_TRANSLATOR_KEY'))

def translate_text(text, to_language):
    input_text = TextTranslationInput(text=text, to=[to_language])
    result = client.translate(input_text)
    return result[0].translations[0].text