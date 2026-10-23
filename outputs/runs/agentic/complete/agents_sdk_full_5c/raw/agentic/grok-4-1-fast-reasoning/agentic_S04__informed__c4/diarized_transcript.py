import time
import assemblyai as aai
from speech_client import get_client
from speech_models import create_transcription_config

def diarized_transcript(audio_file_path: str) -> list:
    client = get_client()
    config = create_transcription_config(speaker_labels=True)
    transcript = client.transcripts.transcribe(audio_file_path, config)
    
    while transcript.status not in [aai.TranscriptStatus.completed, aai.TranscriptStatus.error]:
        time.sleep(10)
        transcript = client.transcripts.get(transcript.id)
    
    if transcript.status == aai.TranscriptStatus.error:
        raise ValueError(f"Transcription failed: {transcript.error}")
    
    return [
        {
            "speaker": utt.speaker,
            "text": utt.text,
            "start": utt.start,
            "end": utt.end
        }
        for utt in transcript.utterances
    ]