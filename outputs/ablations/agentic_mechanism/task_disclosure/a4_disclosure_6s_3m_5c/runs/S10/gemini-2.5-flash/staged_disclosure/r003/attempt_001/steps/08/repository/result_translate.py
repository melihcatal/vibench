
from google.cloud import translate_v2 as translate

def translate_text(text, target_language="en"):
    """Translates text into the target language using Google Cloud Translation."""
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]

if __name__ == "__main__":
    # Example usage (you would replace this with your actual model output)
    model_output = "Hola, ¿cómo estás?"
    translated_output = translate_text(model_output, target_language="fr")
    print(f"Original: {model_output}")
    print(f"Translated (French): {translated_output}")

    model_output_japanese = "こんにちは、元気ですか？"
    translated_output_english = translate_text(model_output_japanese, target_language="en")
    print(f"Original: {model_output_japanese}")
    print(f"Translated (English): {translated_output_english}")
