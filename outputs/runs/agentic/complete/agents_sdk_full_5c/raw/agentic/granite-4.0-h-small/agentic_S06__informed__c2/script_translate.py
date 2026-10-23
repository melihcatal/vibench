import json
import requests
from typing import Dict

# Reference: Alibaba Cloud Machine Translation (using SDK `alibabacloud_alimt`)
# Provider identifier: alibabacloud_alimt import and env variables
from alibabacloud_alimt import TranslateTextRequest, AcsClient
from alibabacloud_tea_util.model import RuntimeOptions

# Expected environment variables for Alibaba Cloud
ALIBABA_ACCESS_KEY_ID = os.getenv("ALIBABA_ACCESS_KEY_ID")
ALIBABA_ACCESS_KEY_SECRET = os.getenv("ALIBABA_ACCESS_KEY_SECRET")
ALIBABA_REGION = os.getenv("ALIBABA_REGION", "cn-shanghai")

# Build the client once (singleton pattern)
class TranslateClient:
    _instance: 'TranslateClient' = None
    def __new__(cls):
        if cls._instance is None:
            if not all([ALIBABA_ACCESS_KEY_ID, ALIBABA_ACCESS_KEY_SECRET]):
                raise RuntimeError("Set ALIBABA_ACCESS_KEY_ID and ALIBABA_ACCESS_KEY_SECRET")
            cls._instance = super().__new__(cls)
            cls._instance.client = AcsClient(
                access_key_id=ALIBABA_ACCESS_KEY_ID,
                access_key_secret=ALIBABA_ACCESS_KEY_SECRET,
                region_id=ALIBABA_REGION,
            )
        return cls._instance

    def translate(self, source: str, target_lang: str = "en") -> Dict[str, Any]:
        """Translate Chinese (zh) to English (or any target) using Alibaba Cloud API.
        Returns a minimal representation of the JSON response for integration testing.
        """
        request = TranslateTextRequest.TranslateTextRequest()
        request.source_language = "zh"
        request.target_language = target_lang
        request.text = source
        runtime = RuntimeOptions()
        response = self.client.do_action_with_exception(request, runtime)
        # Decode bytes response and parse as JSON
        result = json.loads(response.decode('utf-8'))
        # The SDK returns a structure like {'translated': '...'} in success cases
        return result

    @staticmethod
def get_client() -> 'TranslateClient':
        return TranslateClient._instance

# Utility callable for one‑line use
translate_text = TranslateClient.get_client().translate
