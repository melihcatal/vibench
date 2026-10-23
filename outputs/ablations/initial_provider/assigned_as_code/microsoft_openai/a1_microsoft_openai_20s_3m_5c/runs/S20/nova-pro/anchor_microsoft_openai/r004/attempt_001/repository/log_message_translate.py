from azure.identity import DefaultAzureCredential
from azure.cognitiveservices.language.text.translation import TextTranslationClient
from msrest.authentication import CognitiveServicesCredentials


def log_message_translate(log_text, target_language, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        client = TextTranslationClient(credentials=CognitiveServicesCredentials(credential.get_token('https://api.cognitive.microsoft.com/sts/v1.0/issueToken').token))
        translated_text = client.translate([log_text], target_language)[0].translations[0].text
        return translated_text
