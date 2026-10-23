import os
import azure.cognitiveservices.speech as speechsdk  # Provider SDK import


def generate_spoken_brief(text: str, output_filepath: str = "spoken_brief.wav"):
    """
    Generates a spoken brief from the model output using Azure AI Speech TTS.
    """
    speech_key = os.environ.get(
        "AZURE_SPEECH_KEY"
    )  # Provider-specific environment variable
    service_region = os.environ.get(
        "AZURE_SPEECH_REGION"
    )  # Provider-specific environment variable

    if not speech_key or not service_region:
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION must be set.")

    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=service_region
    )
    speech_config.speech_synthesis_voice_name = (
        "en-US-JennyNeural"  # Provider-specific voice name
    )

    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_filepath)
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )

    result = speech_synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Speech synthesized to {output_filepath} for text [{text}]")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")
