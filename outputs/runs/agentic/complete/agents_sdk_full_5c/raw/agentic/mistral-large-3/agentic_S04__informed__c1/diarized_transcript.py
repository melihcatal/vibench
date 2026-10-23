from speech_client import get_assemblyai_client
from speech_models import DiarizedTranscript

def get_diarized_transcript(transcript_id: str) -> DiarizedTranscript:
    client = get_assemblyai_client()
    transcript = client.transcripts.get(transcript_id)
    if not transcript.utterances:
        raise ValueError("No speaker diarization data available.")
    
    return DiarizedTranscript(
        transcript_id=transcript.id,
        utterances=[
            {
                "speaker": utterance.speaker,
                "text": utterance.text,
                "start": utterance.start,
                "end": utterance.end
            }
            for utterance in transcript.utterances
        ]
    )