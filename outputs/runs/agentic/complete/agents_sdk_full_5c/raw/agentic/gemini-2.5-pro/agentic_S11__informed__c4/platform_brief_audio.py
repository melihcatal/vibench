import os
import azure.cognitiveservices.speech as speechsdk

def generate_audio_briefing(text: str, output_path: str):
    """
    Generates a spoken audio file from text using Azure AI Speech service.
    
    Args:
        text: The text to synthesize into speech.
        output_path: The path to save the resulting audio file (e.g., "briefing.wav").
    """
    speech_key = os.environ["AZURE_SPEECH_KEY"]
    speech_region = os.environ["AZURE_SPEECH_REGION"]

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    # Set a natural-sounding voice
    speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)

    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Speech synthesized for text [{text[:30]}...] and saved to [{output_path}]")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print(f"Error details: {cancellation_details.error_details}")
        raise RuntimeError("Speech synthesis failed.")
