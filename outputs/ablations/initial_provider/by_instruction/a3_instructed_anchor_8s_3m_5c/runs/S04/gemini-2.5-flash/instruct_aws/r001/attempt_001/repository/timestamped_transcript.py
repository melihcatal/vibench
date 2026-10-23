from speech_client import get_transcribe_client
from speech_models import TimestampRequest, TranscriptionResult
import requests

def get_timestamped_transcript(request: TimestampRequest) -> TranscriptionResult:
    transcribe_client = get_transcribe_client()
    response = transcribe_client.get_transcription_job(
        TranscriptionJobName=request.job_name
    )
    
    status = response['TranscriptionJob']['TranscriptionJobStatus']
    if status == 'COMPLETED':
        transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
        # AWS Transcribe provides a JSON file with word-level timestamps
        full_transcript_json = requests.get(transcript_uri).json()
        
        segments = []
        if 'results' in full_transcript_json and 'items' in full_transcript_json['results']:
            for item in full_transcript_json['results']['items']:
                if item['type'] == 'pronunciation':
                    segments.append({
                        'word': item['alternatives'][0]['content'],
                        'start_time': item['start_time'],
                        'end_time': item['end_time']
                    })
        
        return TranscriptionResult(
            job_name=request.job_name,
            status=status,
            transcript_uri=transcript_uri,
            transcript_text=full_transcript_json['results']['transcripts'][0]['transcript'],
            segments=segments
        )
    else:
        return TranscriptionResult(job_name=request.job_name, status=status)
