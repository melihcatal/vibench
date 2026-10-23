from google.cloud import texttospeech
from speech_client import get_tts_client
from speech_models import SynthesisRequest


def save_audio(request: SynthesisRequest, output_filename: str) -> None:
    client = get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(text=request.text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )
    if request.voice:
        voice.name = request.voice.name

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filename}"')
