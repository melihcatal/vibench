from speech_client import get_openai_client, get_transcription_model, open_audio


def diarized_transcript(audio_path, prompt="Include speakers when possible."):
    client = get_openai_client()
    with open_audio(audio_path) as audio:
        return client.audio.transcriptions.create(
            model=get_transcription_model(),
            file=audio,
            prompt=prompt,
            response_format="verbose_json",
        )
