import azure.cognitiveservices.speech as speechsdk
import os


def generate_platform_brief_audio(text: str, config: dict = None, output_file: str = "output.wav") -> dict:
    config = config or {}
    speech_key = config.get("AZURE_SPEECH_KEY") or os.getenv("AZURE_SPEECH_KEY")
    service_region = config.get("AZURE_SPEECH_REGION") or os.getenv("AZURE_SPEECH_REGION")

    if not speech_key or not service_region:
        raise ValueError("Azure Speech Service key and region not found in config or environment variables.")

    # Configure the speech synthesis
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    
    # You can specify a voice, e.g., "en-US-AvaMultilingualNeural"
    # A list of supported voices can be found here: 
    # https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=text-to-speech#standard-voices
    speech_config.speech_synthesis_voice_name = config.get("AZURE_SPEECH_VOICE_NAME", "en-US-JennyNeural")

    # Use the default speaker as audio output. This will play the audio.
    # To save to a file, use AudioOutputConfig.from_wav_file(output_file)
    audio_config = speechsdk.AudioOutputConfig(filename=output_file)

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    try:
        result = speech_synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return {"status": "success", "audio_file": output_file, "message": "Speech synthesis completed."}
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            return {"status": "cancelled", "error": cancellation_details.error_details, "reason": cancellation_details.reason}
    except Exception as e:
        return {"status": "error", "error": str(e)}

    return {"status": "error", "message": "An unknown error occurred during speech synthesis."}
