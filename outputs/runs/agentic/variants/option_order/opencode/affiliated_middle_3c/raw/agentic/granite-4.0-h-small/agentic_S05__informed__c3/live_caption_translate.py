import asyncio
from google.cloud import translate_v3 as translate


class LiveCaptionTranslate:
    """
    Translates live streaming transcription into another language using Google Cloud Translation.
    Provider: Cloud Translation (service=Google Cloud Translation)
    Configuration:
        GOOGLE_APPLICATION_CREDENTIALS must point to a service account key JSON.
    """

    def __init__(self, target_language_code: str = "es"):  # default to Spanish
        self.client = translate.TranslationServiceClient()
        self.target_language_code = target_language_code

    async def translate_stream(self, transcript_stream):
        """
        Streams translation of interim/final transcription chunks.
        Yields:
            dict: translated text with original language metadata
        """
        parent = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/global"
        for chunk in transcript_stream:
            response = self.client.translate_text(
                request={
                    "contents": [chunk],
                    "target_language_code": self.target_language_code,
                    "parent": parent,
                }
            )
            translation = response.translations[0]
            yield {
                "original": chunk,
                "translation": translation.translated_text,
                "language": self.target_language_code,
            }


if __name__ == "__main__":
    # Example usage with a dummy generator
    async def dummy_stream():
        for i in range(5):
            yield f"Chunk {i} to translate"

    translator = LiveCaptionTranslate()
    asyncio.run(translator.translate_stream(dummy_stream()))
