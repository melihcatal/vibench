from google.cloud import texttospeech
from model_models import ModelConfig, AudioOutput

def generate_platform_brief_audio(
    text: str, config: ModelConfig, language_code: str = "en-US", voice_name: str = "en-US-Standard-A"
) -> AudioOutput:
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the language and SSML voice type
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name, # Example: 'en-US-Standard-A', 'en-GB-Wavenet-B'
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL, # Example: MALE, FEMALE, NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    return AudioOutput(
        audio_content=response.audio_content,
        mime_type="audio/mp3"
    )
