# translate_transcript.py
import os
from typing import Dict, Any

# Use DashScope SDK for translation of completed transcript segments
from dashscope import alimt  # type: ignore

# Load configuration from environment variables
ALIBABA_CLOUD_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_CLOUD_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")


def translate_transcript(
    transcript_segments: List[str], target_lang: str = "es"
) -> Dict[str, Any]:
    """Translates transcript segments to the target language.

    Uses Alibaba Cloud Machine Translation API as the concrete provider.
    Returns a dictionary containing original and translated text.
    """
    client = alimt.Client(
        endpoint="mt.cn-hangzhou.aliyuncs.com",
        access_key_id=ALIBABA_CLOUD_ACCESS_KEY_ID,
        access_key_secret=ALIBABA_CLOUD_ACCESS_KEY_SECRET,
    )
    # Build translation request (batch up to 1000 characters per request)
    batch = [seg for seg in transcript_segments if seg]  # filter empty
    response = client.translate_text(text=batch, target_lang=target_lang)
    # Normalize response into consistent structure
    normalized = [
        {
            "original": seg,
            "translated": seg_res["translated"],
        }
        for seg, seg_res in zip(batch, response["data"]["translated"])
    ]
    return {"translations": normalized}
