from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

def translate_invoice_note(note_text, target_language="es"):
    client = TextTranslationClient(
        endpoint="https://<your-custom-subdomain>.cognitiveservices.azure.com",
        credential=AzureKeyCredential("<your-api-key>")
    )
    result = client.translate([note_text], target_language)[0]
    return result.translations[0].text