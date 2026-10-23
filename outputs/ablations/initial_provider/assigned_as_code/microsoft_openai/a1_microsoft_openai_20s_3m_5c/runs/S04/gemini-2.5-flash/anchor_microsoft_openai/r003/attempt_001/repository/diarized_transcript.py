from speech_client import AzureSpeechClient
from speech_models import TranscriptionConfig, TranscriptionPayload, TranscriptionJob, DiarizationResult
from poll_transcription import poll_transcription

def diarized_transcript(payload: TranscriptionPayload, config: TranscriptionConfig) -> DiarizationResult:
    client = AzureSpeechClient(config)
    
    properties = {
        'diarization': {'speakers': {'minCount': 1, 'maxCount': 10}}
    }
    
    # Submit the transcription job with diarization properties
    submit_response = client.submit_transcription_job(
        display_name=config.job_name or 'diarized_transcription',
        locale=payload.language_code,
        content_urls=[payload.audio_uri],
        properties=properties
    )

    job = TranscriptionJob(
        job_id=submit_response['self'],
        status=submit_response['status'].upper()
    )

    # Poll for the transcription result
    completed_job = poll_transcription(job, config)

    if completed_job.status == 'SUCCEEDED' and completed_job.results:
        # Assuming Azure's diarization output is structured with 'speaker' in segments
        # This part might need adjustment based on actual Azure STT JSON output for diarization
        segments = []
        for phrase in completed_job.results.get('recognizedPhrases', []):
            speaker_id = phrase.get('speaker') # Speaker ID for the entire phrase
            offset_seconds = int(phrase['offsetInTicks']) / 10_000_000
            duration_seconds = int(phrase['durationInTicks']) / 10_000_000
            text = phrase['nBest'][0]['display']

            segments.append({
                "start_time": str(offset_seconds),
                "end_time": str(offset_seconds + duration_seconds),
                "text": text,
                "speaker": speaker_id
            })
        return DiarizationResult(segments=segments)
    else:
        raise Exception(f"Diarized transcription failed or returned no results: {completed_job.status}")
