import azure.cognitiveservices.speech as speechsdk
from typing import Dict, Any

def generate_reviewer_brief_audio(text_brief: str, output_filepath: str, config: Dict[str, Any] = None) -> bool:
    config = config or {}
    # Azure AI Speech Configuration
    # Environment variables should be set for AZURE_SPEECH_KEY, AZURE_SPEECH_REGION
    # or passed via config. Here we use config for consistency.
    
    speech_key = config.get("azure_speech_key")
    service_region = config.get("azure_speech_region")

    if not speech_key or not service_region:
        print("Error: Azure Speech key or region not provided.")
        return False

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    
    # Configure voice, e.g., "en-US-JennyNeural"
    # A list of voices can be found here: https://docs.microsoft.com/azure/cognitive-services/speech-service/language-support#standard-voices
    speech_config.speech_synthesis_voice_name = config.get("azure_speech_voice_name", "en-US-JennyNeural")

    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_filepath)

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    try:
        result = speech_synthesizer.speak_text_async(text_brief).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"Speech synthesized to [{output_filepath}] for text: {text_brief[:50]}...")
            return True
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f"Speech synthesis canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(f"Error details: {cancellation_details.error_details}")
            return False
    except Exception as e:
        print(f"Error synthesizing speech: {e}")
        return False
    return False # Should not reach here
