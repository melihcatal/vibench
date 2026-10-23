from google.cloud import texttospeech
from model_models import ModelResponse

def platform_brief_audio(model_response: ModelResponse, audio_file_path: str = "briefing.mp3"):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=model_response.text)

    # Configure the voice parameters
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Configure the audio format
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Write the audio content to a file
    with open(audio_file_path, "wb") as out:
        out.write(response.audio_content)

    return {"text": model_response.text, "audio_file_path": audio_file_path}
