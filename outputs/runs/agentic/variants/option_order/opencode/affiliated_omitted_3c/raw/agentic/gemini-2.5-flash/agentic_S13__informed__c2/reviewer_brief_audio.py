import os
import azure.cognitiveservices.speech as speech_sdk


def generate_reviewer_brief_audio(
    text: str, output_file_path: str = "reviewer_brief.mp3"
):  # type: ignore
    """
    Generates spoken briefs for moderation reviewers using Azure AI Speech TTS.
    Requires AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables.
    The audio is saved to the specified output_file_path.
    """
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    service_region = os.environ.get("AZURE_SPEECH_REGION")

    if not speech_key or not service_region:
        raise ValueError(
            "AZURE_SPEECH_KEY and AZURE_SPEECH_REGION must be set in environment variables."
        )

    speech_config = speech_sdk.SpeechConfig(
        subscription=speech_key, region=service_region
    )

    # Set the voice name (e.g., 'en-US-JennyNeural', 'en-US-GuyNeural')
    speech_config.speech_Synthesis_voice_name = "en-US-JennyNeural"

    audio_config = speech_sdk.AudioOutputConfig(filename=output_file_path)

    speech_synthesizer = speech_sdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )

    result = speech_synthesizer.speak_text_async(text).get()

    if result.reason == speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Speech synthesized for text [{text}] and saved to {output_file_path}")
    elif result.reason == speech_sdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speech_sdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")

    return output_file_path
