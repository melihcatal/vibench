from azure.ai.translation.text import TextTranslationClient, TranslatorCredential

translator_client = TextTranslationClient(
    endpoint=os.getenv("AZURE_TRANSLATOR_ENDPOINT"),
    credential=TranslatorCredential(os.getenv("AZURE_TRANSLATOR_KEY")),
)
