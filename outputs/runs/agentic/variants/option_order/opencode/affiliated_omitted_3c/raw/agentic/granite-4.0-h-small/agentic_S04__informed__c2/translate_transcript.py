# LATER-STEP: translate_transcript.py

# Integration with Alibaba Cloud Machine Translation API
# Provider: Alibaba Cloud Translation (ALIBABA_CLOUD_ACCESS_KEY_ID / SECRET)
import os
from alibabacloud_tea_util_20210226.models import RuntimeOptions
from alibabacloud_mtz_20210226.client import Client as MtzClient
from alibabacloud_mtz_20210226.models import TranslateRequest


class AlibabaTranslator:
    """Thin wrapper around Alibaba Cloud Machine Translation API."""

    def __init__(self):
        access_key_id = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
        access_key_secret = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        if not (access_key_id and access_key_secret):
            raise RuntimeError(
                "ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET must be set"
            )
        self.client = MtzClient(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            endpoint="mtz.cn-shanghai.aliyuncs.com",
        )

    def translate(
        self, source_text: str, target_lang: str = "en", source_lang: str = "zh"
    ) -> str:
        """Translate a text segment to the target language."""
        request = TranslateRequest(
            source_text=source_text,
            source_lang_code=source_lang,
            target_lang_code=target_lang,
        )
        runtime = RuntimeOptions()
        response = self.client.translate(request, runtime)
        # Response format: {"translated_text": "..."}
        return response.body["translated_text"]


# Simple helper function for one-off translations
translate_segment = AlibabaTranslator().translate
