from google.cloud import texttospeech

def generate_audio_preview(payload, config=None):
    config = config or {}
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=payload["text"])
    voice = texttospeech.VoiceSelectionParams(
        language_code=payload["language_code"],
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    return {
        "text": payload["text"],
        "language_code": payload["language_code"],
        "audio_content": response.audio_content  # This will be bytes, can be saved to a file
    }
