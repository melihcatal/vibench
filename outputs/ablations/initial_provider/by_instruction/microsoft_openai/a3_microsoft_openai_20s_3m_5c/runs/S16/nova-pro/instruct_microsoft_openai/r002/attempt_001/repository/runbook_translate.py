from azure.ai.translator.text import TranslatorClient, TranslatorTextConfig
from azure.core.credentials import AzureKeyCredential

def runbook_translate(text, to_language):
    credential = AzureKeyCredential("<your-translator-key>")
    client = TranslatorClient(endpoint="https://<your-translator-endpoint>.cognitiveservices.azure.com/", credential=credential)
    config = TranslatorTextConfig(to=[to_language])
    result = client.translate(text, config=config)
    return result[0].translations[0].text