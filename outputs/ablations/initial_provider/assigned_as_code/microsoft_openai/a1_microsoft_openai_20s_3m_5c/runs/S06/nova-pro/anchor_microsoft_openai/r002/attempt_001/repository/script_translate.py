from azure.ai.translation.text import TextTranslationClient, TextTranslationInput
from azure.core.credentials import AzureKeyCredential

def translate_script(script, config):
    credential = AzureKeyCredential(config['api_key'])
    client = TextTranslationClient(endpoint=config['endpoint'], credential=credential)
    result = client.translate([TextTranslationInput(text=script, to=['en'])])
    return result[0].translations[0].text