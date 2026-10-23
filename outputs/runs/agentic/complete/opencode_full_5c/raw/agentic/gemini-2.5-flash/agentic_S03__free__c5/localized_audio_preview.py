from translation_client import get_text_to_speech_client
from google.cloud.texttospeech import (
    SynthesisInput,
    VoiceSelectionParams,
    AudioConfig,
    AudioEncoding,
)


def localized_audio_preview(text: str, language_code: str) -> bytes:
    client = get_text_to_speech_client()

    synthesis_input = SynthesisInput(text=text)

    # Select the language and SSML voice type
    voice = VoiceSelectionParams(
        language_code=language_code, ssml_gender=VoiceSelectionParams.SsmlGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = AudioConfig(audio_encoding=AudioEncoding.MP3)

    response = client.synthesize_speech(
        request={
            "input": synthesis_input,
            "voice": voice,
            "audio_config": audio_config,
        }
    )

    # The response's audio_content is binary. You can save it to a file or stream it.
    return response.audio_content
