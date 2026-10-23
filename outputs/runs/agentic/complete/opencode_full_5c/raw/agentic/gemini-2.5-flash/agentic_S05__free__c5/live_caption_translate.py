from google.cloud import translate_v2 as translate
from speech_models import SpeechRecognitionResult

# Google Cloud Translation uses the `google.cloud.translate_v2` SDK
# and `translate.Client` for its operations.


def translate_caption_chunk(text: str, target_language: str = "es") -> str:
    """
    Translates a single caption chunk to the target language using Google Cloud Translation API.

    Args:
        text: The text chunk to translate.
        target_language: The target language code (e.g., "es" for Spanish, "fr" for French).

    Returns:
        The translated text.
    """
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    # print(f"Text: {result['input']}")
    # print(f"Translation: {result['translatedText']}")
    # print(f"Detected source language: {result['detectedSourceLanguage']}")

    return result["translatedText"]


async def live_caption_translate_stream(
    caption_stream_generator, target_language: str = "es"
):
    """
    Asynchronously translates a stream of live captions.

    Args:
        caption_stream_generator: An async generator yielding SpeechRecognitionResult objects.
        target_language: The target language for translation.

    Yields:
        Tuple[str, str]: Original caption and its translation.
    """
    print(f"Starting live caption translation to {target_language}...")
    async for caption_result in caption_stream_generator:
        if caption_result.is_final and caption_result.transcript.strip():
            translated_text = translate_caption_chunk(
                caption_result.transcript, target_language
            )
            print(
                f"Original: {caption_result.transcript} -> Translated ({target_language}): {translated_text}"
            )
            yield caption_result.transcript, translated_text
