from google.cloud import translate_v2 as translate


class ResultTranslator:
    def __init__(self):
        self.client = translate.Client()

    def translate_to(self, text, target="en"):
        result = self.client.translate(text, target_language=target)
        return result["translatedText"]

    def translate_from(self, text, source="auto"):
        result = self.client.translate(text, source_language=source)
        return result["translatedText"]


if __name__ == "__main__":
    translator = ResultTranslator()
    french = "Bonjour"
    print("French -> English:", translator.translate_to(french))
    english = "Hello"
    print("English -> German:", translator.translate_from(english, target="de"))
