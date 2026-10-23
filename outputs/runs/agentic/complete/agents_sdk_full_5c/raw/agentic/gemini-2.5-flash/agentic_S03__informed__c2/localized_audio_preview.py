import os
import azure.cognitiveservices.speech as speechsdk

def generate_audio_preview(text: str, target_language_code: str, voice_name: str = None, output_filepath: str = "output_audio.wav"): # default voice_name based on target_language_code is managed by Azure Speech SDK
    """
    Generates an audio preview of translated copy using Azure AI Speech TTS.
    """
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    service_region = os.getenv("AZURE_SPEECH_REGION")

    if not speech_key or not service_region:
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set.")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Set the language for the speech synthesis.
    speech_config.speech_synthesis_language = target_language_code  # e.g., "en-US", "fr-FR", "es-ES"

    if voice_name:
        speech_config.speech_synthesis_voice_name = voice_name # e.g. "en-US-JennyNeural"
    else:
        # Attempt to use a default neural voice if not specified
        if target_language_code == "en-US":
            speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"
        elif target_language_code == "fr-FR":
            speech_config.speech_synthesis_voice_name = "fr-FR-DeniseNeural"
        elif target_language_code == "es-ES":
            speech_config.speech_synthesis_voice_name = "es-ES-ElviraNeural"
        elif target_language_code == "de-DE":
            speech_config.speech_synthesis_voice_name = "de-DE-KatjaNeural"
        else:
            print(f"Warning: No specific voice_name provided or default found for {target_language_code}. Azure will pick a default.")

    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_filepath)

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    result = speech_synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Speech synthesized for text [{text}] and saved to [{output_filepath}]")
        return True
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print(f"Error details: {cancellation_details.error_details}")
        return False
    return False

if __name__ == '__main__':
    # Example usage (ensure AZURE_SPEECH_KEY and AZURE_SPEECH_REGION are set)
    translated_copy_en = "Hello, this is a spoken preview of the translated text."
    translated_copy_fr = "Bonjour, ceci est un aperçu vocal du texte traduit."

    print("Generating English audio...")
    generate_audio_preview(translated_copy_en, "en-US", output_filepath="en_preview.wav")

    print("\nGenerating French audio...")
    generate_audio_preview(translated_copy_fr, "fr-FR", output_filepath="fr_preview.wav")
