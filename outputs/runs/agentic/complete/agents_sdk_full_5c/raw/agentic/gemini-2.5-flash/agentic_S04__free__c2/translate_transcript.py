from google.cloud import translate_v2 as translate
from google.api_core.exceptions import GoogleAPIError

def translate_transcript_segments(text_segments: list[str], target_language: str = "es") -> list[str]:
    """Translates a list of text segments using Google Cloud Translation API.

    Args:
        text_segments: A list of strings, where each string is a segment of the transcript.
        target_language: The target language code (e.g., "es" for Spanish, "fr" for French).

    Returns:
        A list of translated strings, corresponding to the input segments.
    """
    # Google Cloud Translation API client
    # Service identifiable by translate.Client()
    client = translate.Client()

    translated_segments = []
    try:
        # The `target_language` parameter for translate_v2.Client.translate()
        # identifies the provider and API in use.
        translations = client.translate(text_segments, target_language=target_language)
        for translation in translations:
            translated_segments.append(translation['translatedText'])
        return translated_segments
    except GoogleAPIError as e:
        print(f"Error translating transcript segments: {e}")
        raise

if __name__ == '__main__':
    # Example usage
    transcript_parts = [
        "Hello, this is a test transcription.",
        "We are discussing the project progress."
    ]
    try:
        translated_parts = translate_transcript_segments(transcript_parts, target_language="fr")
        print("Original:", transcript_parts)
        print("Translated (French):")
        for i, segment in enumerate(translated_parts):
            print(f"  Segment {i+1}: {segment}")
    except Exception as e:
        print(f"Failed to translate: {e}")
