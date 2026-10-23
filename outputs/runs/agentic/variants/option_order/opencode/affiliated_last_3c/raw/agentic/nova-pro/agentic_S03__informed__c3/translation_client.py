import os


def get_translation_client(provider):
    if provider == "deepl":
        auth_key = os.getenv("DEEPL_AUTH_KEY")
        return deepl.Translator(auth_key)
    elif provider == "google":
        return translate.TranslationServiceClient()
    elif provider == "azure":
        credential = TranslatorCredential(os.getenv("AZURE_TRANSLATOR_KEY"))
        return TextTranslationClient(
            endpoint=f"https://{os.getenv('AZURE_TRANSLATOR_REGION')}.api.cognitive.microsofttranslator.com",
            credential=credential,
        )
    elif provider == "amazon":
        return boto3.client("translate")
