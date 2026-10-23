import azure.ai.translation.text as az_translate


def translate_text(text):
    client = az_translate.TextTranslationClient(
        endpoint=os.getenv("AZURE_TRANSLATOR_ENDPOINT"),
        credential=az_translate.AzureKeyCredential(os.getenv("AZURE_TRANSLATOR_KEY")),
    )
    result = client.translate(text, to="en")
    return result[0].translations[0].text
