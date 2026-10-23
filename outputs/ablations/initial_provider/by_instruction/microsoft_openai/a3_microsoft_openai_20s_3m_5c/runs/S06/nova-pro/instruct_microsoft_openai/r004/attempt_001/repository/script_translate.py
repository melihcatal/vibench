from azure.cognitiveservices.language.text.translation import TextTranslationClient
from msrest.authentication import CognitiveServicesCredentials

def translate_text(text: str, target_language: str) -> str:
    subscription_key = "YOUR_TRANSLATOR_KEY"
    endpoint = "https://api.cognitive.microsofttranslator.com/"
    client = TextTranslationClient(CognitiveServicesCredentials(subscription_key), endpoint)
    result = client.translate([text], target_language)[0]
    return result.translations[0].text