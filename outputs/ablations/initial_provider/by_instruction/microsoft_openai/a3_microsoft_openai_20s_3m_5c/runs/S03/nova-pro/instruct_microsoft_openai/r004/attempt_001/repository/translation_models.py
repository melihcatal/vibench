from azure.ai.translation.text import TextTranslationClient, TextTranslationInput

class TranslationClient:
    def __init__(self):
        self.client = TextTranslationClient(endpoint=os.getenv('AZURE_TRANSLATE_ENDPOINT'), credential=os.getenv('AZURE_TRANSLATE_KEY'))

    def translate(self, text, to_language):
        input_text = TextTranslationInput(text=text, to=[to_language])
        result = self.client.translate([input_text])
        return result[0].translations[0].text