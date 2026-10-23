# [LATER-STEP] reviewer_brief_audio.py
"""Generate spoken briefs for moderation reviewers using Alibaba Text-to-Speech SDK.
Creates an audio file (or URL) summarizing the moderation decision for a reviewer.
"""

import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from safety_client import normalize_response


async def generate_reviewer_brief(decision: dict, reviewer_id: str):
    """Create a short audio brief describing the moderation decision."""
    authenticator = IAMAuthenticator(os.getenv("IBM_TTS_APIKEY"))
    tts = TextToSpeechV1(authenticator=authenticator)
    tts.set_service_url(os.getenv("IBM_TTS_URL"))
    # Simple text message summarizing the decision
    text = f"Reviewer {reviewer_id}: The message was flagged as {decision.get('label', 'safe')}. Please review as needed."
    with open("reviewer_brief.wav", "wb") as audio_file:
        audio_file.write(
            tts.synthesize(text=text, accept="audio/wav", voice="zh-CN_LiNaVoiceStd")
            .get_result()
            .get_result()
        )
    return "reviewer_brief.wav"
