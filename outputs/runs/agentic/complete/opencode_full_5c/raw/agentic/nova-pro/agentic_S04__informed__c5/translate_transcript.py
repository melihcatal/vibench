from azure.ai.translation.text import TextTranslationClient, TranslatorCredential


def translate_transcript(transcript):
    credential = TranslatorCredential(os.getenv("AZURE_TRANSLATOR_KEY"))
    client = TextTranslationClient(
        credential=credential,
        endpoint=f"https://{os.getenv('AZURE_TRANSLATOR_REGION')}.api.cognitive.microsofttranslator.com",
    )
    result = client.translate(content=transcript, to=["es"])
    return result[0].translations[0].text
