import time
from speech_client import get_speech_client
from speech_models import stt_config

def diarized_transcript(audio_path: str) -> str:
    client = get_speech_client()
    audio_url = client.upload(audio_path)
    config = {
        'audio_url': audio_url,
        **stt_config(speaker_diarization=True)
    }
    transcript = client.transcripts.create(config)
    
    while transcript.status not in ['completed', 'error']:
        time.sleep(10)
        transcript = client.transcripts.get(transcript.id)
    
    if transcript.status == 'error':
        raise ValueError(f'Transcription error: {transcript.error}')
    
    if not hasattr(transcript, 'utterances') or not transcript.utterances:
        return transcript.text
    
    formatted = '\n'.join([
        f'Speaker {utterance.speaker}: {utterance.text}'
        for utterance in transcript.utterances
    ])
    return formatted