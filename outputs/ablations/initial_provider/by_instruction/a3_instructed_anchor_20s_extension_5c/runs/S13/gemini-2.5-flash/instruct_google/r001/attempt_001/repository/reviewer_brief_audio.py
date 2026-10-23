from safety_client import SafetyClient
from safety_models import AudioBriefResult
from google.cloud import texttospeech_v1

def generate_reviewer_brief_audio(brief_text: str) -> AudioBriefResult:
    client = SafetyClient()
    texttospeech_client = client.get_texttospeech_client()

    # Set the text input to be synthesized
    synthesis_input = texttospeech_v1.SynthesisInput(text=brief_text)

    # Build the voice request, select the language code (e.g., "en-US") and the ssml
    # voice gender (e.g., ssml_gender=texttospeech_v1.SsmlVoiceGender.FEMALE)
    voice = texttospeech_v1.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech_v1.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech_v1.AudioConfig(
        audio_encoding=texttospeech_v1.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    # Google Cloud Text-to-Speech API is the concrete external provider.
    response = texttospeech_client.synthesize_speech(
        request={"input": synthesis_input, "voice": voice, "audio_config": audio_config}
    )

    # The response's audio_content is binary. It can be saved to a file or streamed.
    audio_content_bytes = response.audio_content

    return AudioBriefResult(
        text=brief_text,
        audio_content=audio_content_bytes,
        provider="Google Cloud Text-to-Speech API"
    )

