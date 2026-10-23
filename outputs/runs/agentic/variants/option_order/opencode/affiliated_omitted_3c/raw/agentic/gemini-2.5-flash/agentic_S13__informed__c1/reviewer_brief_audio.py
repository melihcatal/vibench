import azure.cognitiveservices.speech as speechsdk
import os


def generate_reviewer_brief_audio(text: str, output_filepath: str):
    """
    Generates spoken briefs for moderation reviewers using Azure AI Speech TTS.
    """
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    service_region = os.environ.get("AZURE_SPEECH_REGION")

    if not speech_key or not service_region:
        raise ValueError(
            "AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set."
        )

    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=service_region
    )
    speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"  # A common voice

    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_filepath)
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )

    result = speech_synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return f"Speech synthesized to {output_filepath}"
    else:
        cancellation_details = result.cancellation_details
        return (
            f"Speech synthesis canceled: {cancellation_details.reason}. "
            f"Error details: {cancellation_details.error_details}"
        )
