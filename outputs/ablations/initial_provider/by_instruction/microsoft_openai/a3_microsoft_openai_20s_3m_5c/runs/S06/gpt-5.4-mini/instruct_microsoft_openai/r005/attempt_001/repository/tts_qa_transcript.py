from speech_client import transcription_client


def transcribe_qa_sample(audio_file):
    response = transcription_client().audio.transcriptions.create(model="gpt-4o-mini-transcribe", file=audio_file)
    return response.text
