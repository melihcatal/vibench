from google.cloud import translate_v2 as translate

client = translate.Client()

def translate_script(script: str, target_lang: str = "es"):
    """Translate a narration script to the target language."""
    result = client.translate(script, target_language=target_lang)
    return result["translatedText"]

if __name__ == "__main__":
    sample = "Hello, world! This is a narration for our podcast."
    translated = translate_script(sample, target_lang="fr")
    print("Translated:", translated)
