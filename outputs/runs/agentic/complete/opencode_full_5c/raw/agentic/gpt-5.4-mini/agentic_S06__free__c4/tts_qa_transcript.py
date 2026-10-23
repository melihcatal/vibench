from speech_client import get_client, transcription_model


def transcribe_tts_audio(audio_bytes, filename="sample.mp3"):
    client = get_client()
    result = client.audio.transcriptions.create(
        model=transcription_model(),
        file=(filename, audio_bytes),
    )
    return result.text
