import os
import azure.cognitiveservices.speech as speechsdk

from translation_models import LocalizedAudioPreviewRequest, LocalizedAudioPreviewResponse

def generate_localized_audio_preview(request: LocalizedAudioPreviewRequest) -> LocalizedAudioPreviewResponse:
    """Generates a spoken preview of translated copy using Azure AI Speech TTS."""
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    speech_region = os.environ.get("AZURE_SPEECH_REGION")

    if not speech_key or not speech_region:
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set.")

    # Configure the Azure Speech SDK
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)

    # Set audio output format
    # https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/rest-text-to-speech?tabs=streaming#audio-outputs
    if request.audio_format == "mp3":
        speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz64KBitRateMonoMp3)
    elif request.audio_format == "wav":
        speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm)
    elif request.audio_format == "ogg":
        speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Ogg16Khz16BitMonoOpus)
    else:
        # Default to WAV if format is not recognized or not specified
        speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm)

    # Determine the voice to use. If not specified, Azure will pick a default for the language.
    # Example voice names: 'en-US-JennyNeural', 'es-ES-ElviraNeural'
    # You can find a full list here: https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#standard-voices
    if request.voice_name:
        speech_config.speech_synthesis_voice_name = request.voice_name
    else:
        # Attempt to set a default neural voice based on language code if no specific voice name is given
        # This is a simplification; a more robust solution would map language codes to specific neural voices.
        if request.language_code.startswith("en-"):
            speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"
        elif request.language_code.startswith("es-"):
            speech_config.speech_synthesis_voice_name = "es-ES-ElviraNeural"
        elif request.language_code.startswith("fr-"):
            speech_config.speech_synthesis_voice_name = "fr-FR-DeniseNeural"
        # Add more language mappings as needed

    audio_data = b''

    # Create a speech synthesizer with no explicit audio output device, so it synthesizes to memory
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    result = speech_synthesizer.speak_text_async(request.text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        audio_data = result.audio_data
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")
            print(f"Did you set the speech resource key and region values?")

    return LocalizedAudioPreviewResponse(
        audio_content=audio_data,
        audio_format=request.audio_format
    )

if __name__ == '__main__':
    # Example usage for testing
    os.environ['AZURE_SPEECH_KEY'] = 'YOUR_AZURE_SPEECH_KEY'     # Replace with your actual key
    os.environ['AZURE_SPEECH_REGION'] = 'YOUR_AZURE_SPEECH_REGION' # Replace with your actual region (e.g., 'westus', 'eastus')

    output_dir = "./audio_previews"
    os.makedirs(output_dir, exist_ok=True)

    # Example 1: English text to WAV
    req1 = LocalizedAudioPreviewRequest(
        text="Hello, this is a preview of the translated text.",
        language_code="en-US",
        audio_format="wav"
    )
    res1 = generate_localized_audio_preview(req1)
    if res1.audio_content:
        file_path = os.path.join(output_dir, f"preview_en.{res1.audio_format}")
        with open(file_path, "wb") as f:
            f.write(res1.audio_content)
        print(f"Generated audio preview: {file_path}")

    # Example 2: Spanish text to MP3 with a specific voice
    req2 = LocalizedAudioPreviewRequest(
        text="Hola, esta es una vista previa del texto traducido.",
        language_code="es-ES",
        voice_name="es-ES-ElviraNeural", # You can try other voices like es-ES-AlvaroNeural
        audio_format="mp3"
    )
    res2 = generate_localized_audio_preview(req2)
    if res2.audio_content:
        file_path = os.path.join(output_dir, f"preview_es.{res2.audio_format}")
        with open(file_path, "wb") as f:
            f.write(res2.audio_content)
        print(f"Generated audio preview: {file_path}")

    # Example 3: French text to OGG
    req3 = LocalizedAudioPreviewRequest(
        text="Bonjour, ceci est un aperçu du texte traduit.",
        language_code="fr-FR",
        audio_format="ogg"
    )
    res3 = generate_localized_audio_preview(req3)
    if res3.audio_content:
        file_path = os.path.join(output_dir, f"preview_fr.{res3.audio_format}")
        with open(file_path, "wb") as f:
            f.write(res3.audio_content)
        print(f"Generated audio preview: {file_path}")
