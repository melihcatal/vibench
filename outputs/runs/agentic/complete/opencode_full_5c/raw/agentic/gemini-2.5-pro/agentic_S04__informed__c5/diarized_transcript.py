from speech_client import get_speech_client
from speech_models import DiarizedTranscript, Utterance


def get_diarized_transcript(audio_file_path: str) -> DiarizedTranscript:
    aai = get_speech_client()
    config = aai.TranscriptionConfig(speaker_labels=True)
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file_path, config)

    if transcript.status == "error":
        return DiarizedTranscript(utterances=[])

    utterances = [
        Utterance(speaker=utterance.speaker, text=utterance.text)
        for utterance in transcript.utterances
    ]
    return DiarizedTranscript(utterances=utterances)
