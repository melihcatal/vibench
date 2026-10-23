import os
import azure.cognitiveservices.speech as speechsdk
from translation_client import azure_speech_synthesizer


def generate_audio_preview(
    text: str, output_filepath: str, voice_name: str = "en-US-JennyNeural"
) -> None:
    if not azure_speech_synthesizer:
        raise ValueError(
            "Azure Speech Synthesizer not initialized. Please set AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables."
        )

    # The voice name specifies the language and gender, e.g., "en-US-JennyNeural" for English (United States), female voice.
    # You can find a list of supported voices in the Azure Speech documentation.
    ssml_text = f"<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='{voice_name[:5]}'><voice name='{voice_name}'>{text}</voice></speak>"

    # Configure audio output to a file
    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_filepath)

    # Create a speech synthesizer with the default speech config and the file output config
    # Note: The azure_speech_synthesizer from translation_client is already initialized with speech_config
    # We need a new synthesizer here to specify output to file, or reconfigure the existing one.
    # For simplicity, creating a new one for this specific file output purpose.
    speech_config_for_file = speechsdk.SpeechConfig(
        subscription=os.getenv("AZURE_SPEECH_KEY"),
        region=os.getenv("AZURE_SPEECH_REGION"),
    )
    file_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config_for_file, audio_config=audio_config
    )

    result = file_synthesizer.speak_ssml_async(ssml_text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Speech synthesized for text [{text}] and saved to [{output_filepath}]")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print(f"Error details: {cancellation_details.error_details}")
            print("Did you set the speech resource key and region values?")
