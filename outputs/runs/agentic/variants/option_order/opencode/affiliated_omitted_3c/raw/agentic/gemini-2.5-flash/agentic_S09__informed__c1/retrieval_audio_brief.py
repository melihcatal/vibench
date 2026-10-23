import os
import azure.cognitiveservices.speech as speechsdk


def generate_audio_brief(
    text: str, output_filepath: str, voice_name: str = "en-US-JennyNeural"
):
    """
    Generates a spoken audio brief from retrieved search results using Azure AI Speech TTS.
    Saves the audio to the specified output_filepath.
    """
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    service_region = os.environ.get("AZURE_SPEECH_REGION")

    if not speech_key or not service_region:
        raise ValueError(
            "AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set."
        )

    # Configure speech synthesis
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=service_region
    )
    speech_config.speech_synthesis_voice_name = voice_name

    # Create an audio configuration that points to an output file
    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_filepath)

    # Create a speech synthesizer
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )

    # Synthesize the text to speech
    result = speech_synthesizer.speak_text_async(text).get()

    # Check the result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Speech synthesized to [{output_filepath}] for text: {text}")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")
