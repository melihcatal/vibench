import os
import azure.cognitiveservices.speech as speechsdk

def generate_audio_preview(text: str, output_file_path: str, voice_name: str = "en-US-JennyNeural"):
    """
    Generates a spoken audio preview of translated text using Azure Speech Service.

    Args:
        text: The translated text to synthesize.
        output_file_path: The path to save the output audio file (e.g., 'preview.wav').
        voice_name: The name of the voice to use for synthesis.
    """
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    speech_region = os.environ.get("AZURE_SPEECH_REGION")

    if not all([speech_key, speech_region]):
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set.")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file_path)

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name=voice_name

    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    
    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        raise RuntimeError(f"Speech synthesis canceled: {cancellation_details.reason}. Details: {cancellation_details.error_details}")
    elif result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
         raise RuntimeError(f"Speech synthesis failed with reason: {result.reason}")

