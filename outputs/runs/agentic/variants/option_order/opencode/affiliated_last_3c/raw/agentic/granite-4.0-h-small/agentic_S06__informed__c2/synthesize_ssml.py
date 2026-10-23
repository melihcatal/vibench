# [SAME-SCENARIO] synthesize_ssml.py
# Azure Speech TTS integration with SSML and prosody controls
import os
from azure.cognitiveservices.speech import SpeechConfig, AudioConfig, SpeechSynthesizer


def synthesize_ssml(
    ssml: str, voice_name: str = "en-US-JennyNeural", prosody_pitch: str = "+0%"
) -> bytes:
    """Synthesize SSML with voice and prosody controls using Azure Cognitive Services Speech SDK.

    Args:
        ssml (str): SSML string to synthesize.
        voice_name (str): Voice to use (default: en-US-JennyNeural).
        prosody_pitch (str): Prosody pitch adjustment (e.g., "+10%" for higher pitch).

    Returns:
        bytes: Synthesized audio as MP3 byte stream.
    """
    speech_config = SpeechConfig(
        subscription=os.getenv("AZURE_SPEECH_KEY"),
        region=os.getenv("AZURE_SPEECH_REGION"),
    )
    speech_config.speech_synthesis_voice_name = voice_name
    # Merge prosody into SSML if not already present
    if "<prosody" not in ssml:
        ssml = (
            f"<speak version='1.0' xml:lang='en-US'><voice name='{voice_name}'>"
            f"<prosody pitch='{prosody_pitch}'>{ssml}</prosody></voice></speak>"
        )
    else:
        ssml = ssml.replace("<speak", f"<speak><voice name='{voice_name}'>")
    audio_config = AudioConfig(output_format="Mp3")
    synthesizer = SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )
    result = synthesizer.speak_ssml_async(ssml).get()
    if result.reason == result.reasons_success:
        return result.audio_data
    else:
        raise RuntimeError(f"SSML synthesis failed: {result.reason}")
