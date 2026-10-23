import os
from typing import Dict
import azure.cognitiveservices.speech as speechsdk


def reviewer_brief_audio(
    brief_text: str, output_path: str = "reviewer_brief.wav"
) -> Dict:
    """Generate spoken briefs for moderation reviewers."""
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    speech_region = os.getenv("AZURE_SPEECH_REGION")

    if not speech_key or not speech_region:
        raise ValueError(
            "Azure Speech credentials not found. Set AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables."
        )

    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=speech_region
    )
    speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)

    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )

    try:
        result = synthesizer.speak_text_async(brief_text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return {
                "success": True,
                "output_path": output_path,
                "text_length": len(brief_text),
                "audio_duration_ms": result.audio_duration.total_seconds() * 1000
                if result.audio_duration
                else 0,
            }
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            return {
                "success": False,
                "error": f"Speech synthesis canceled: {cancellation_details.reason}",
                "error_details": cancellation_details.error_details,
            }
        else:
            return {
                "success": False,
                "error": f"Unknown result reason: {result.reason}",
            }
    except Exception as e:
        return {"success": False, "error": str(e)}
