from google.cloud import translate_v2 as translate
from typing import List


def translate_transcript_segments(
    segments: List[str], target_language: str
) -> List[str]:
    """
    Translates a list of transcript segments to the target language using Google Cloud Translation.
    """
    translate_client = translate.Client()

    translations = []
    for segment in segments:
        result = translate_client.translate(segment, target_language=target_language)
        translations.append(result["translatedText"])
        print(f"Text: {result['input']} -> Translation: {result['translatedText']}")

    return translations


if __name__ == "__main__":
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    transcript_segments = [
        "Hello, how are you today?",
        "I am doing great, thank you for asking.",
        "What are your plans for the weekend?",
    ]
    target_lang = "es"  # Spanish
    translated_segments = translate_transcript_segments(
        transcript_segments, target_lang
    )
    # print("Translated segments:", translated_segments)
