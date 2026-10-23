import os
from azure.ai.translation.text import TextTranslationClient, TextTranslationInput

client = TextTranslationClient(endpoint=f"https://{os.getenv('AZURE_TRANSLATOR_REGION')}.api.cognitive.microsoft.com", credential=os.getenv('AZURE_TRANSLATOR_KEY'))

def batch_translate(texts, to_language):
    input_texts = [TextTranslationInput(text=text, to=[to_language]) for text in texts]
    results = client.translate_batch(input_texts)
    return [result.translations[0].text for result in results]
