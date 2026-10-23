import os
import azure.cognitiveservices.speech as speechsdk

def generate_speech_from_text(text: str, output_filepath: str, voice_name: str = "en-US-AvaMultilingualNeural"):
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    service_region = os.environ.get("AZURE_SPEECH_REGION")

    if not speech_key or not service_region:
        raise ValueError("Azure Speech key and region must be set in environment variables.")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Set the voice name, e.g., "en-US-AvaMultilingualNeural" for US English.
    # You can find a list of supported voices here:
    # https://docs.microsoft.com/azure/cognitive-services/speech-service/language-support#standard-voices
    speech_config.speech_Synthesis_voice_name = voice_name

    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_filepath)

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    result = speech_synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Speech synthesized to {output_filepath} successfully.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print(f"Error details: {cancellation_details.error_details}")
            print("Did you set the speech resource key and region values?")
