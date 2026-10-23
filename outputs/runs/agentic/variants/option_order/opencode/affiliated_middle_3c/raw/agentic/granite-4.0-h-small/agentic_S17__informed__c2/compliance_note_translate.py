# [LATER-STEP] compliance_note_translate.py
# Translate encryption or compliance notes between English and other languages using Alibaba Machine Translation

from alibabacloud_alimt20200521.client import Client as MtClient
from alibabacloud_tea_openapi.models import Config


class NoteTranslator:
    """Translates notes between languages via Alibaba Cloud Machine Translation."""

    def __init__(self):
        # Load credentials from environment variables
        config = Config(
            access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
            access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
            endpoint="api-cn.aliyuncs.com",
        )
        self._client = MtClient(config)

    def translate(self, source_text: str, target_language: str = "zh") -> str:
        """Translates `source_text` into the target language.

        Args:
            source_text (str): Text to translate.
            target_language (str): Target language code (e.g., 'zh', 'es').

        Returns:
            str: Translated text.
        """
        resp = self._client.translate(
            source_text=source_text, target_language=target_language
        )
        # The API returns JSON with a 'data' block containing 'translatedText'
        return resp.get("data", {}).get("translatedText", "Translation failed")


# Simple CLI demo (remove in library usage)
if __name__ == "__main__":
    translator = NoteTranslator()
    original = "The data was encrypted with AES-256 and stored in Cloud KMS."
    print("Original:", original)
    translated = translator.translate(original, target_language="es")
    print("Spanish translation:", translated)
