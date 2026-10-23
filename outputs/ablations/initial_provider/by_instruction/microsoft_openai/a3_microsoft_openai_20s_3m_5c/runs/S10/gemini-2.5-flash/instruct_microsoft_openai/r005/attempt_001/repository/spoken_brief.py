import os
import azure.cognitiveservices.speech as speechsdk

def generate_spoken_brief(text: str, filename: str = "spoken_brief.wav") -> str:
    """
    Generates a spoken brief from the model output using Azure AI Speech.
    """
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    service_region = os.environ.get("AZURE_SPEECH_REGION")

    if not speech_key or not service_region:
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION must be set in environment variables.")

    # Configure the speech synthesizer
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # You can change the voice, e.g., "en-US-AvaMultilingualNeural"
    speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

    # Use an audio file output config
    audio_config = speechsdk.audio.AudioOutputConfig(filename=filename)

    # Create a speech synthesizer
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Synthesize the text to speech
    result = speech_synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return f"Spoken brief saved to {filename}"
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        return f"Speech synthesis canceled: {cancellation_details.reason}. Error details: {cancellation_details.error_details}"
    else:
        return f"Speech synthesis failed: {result.reason}"
