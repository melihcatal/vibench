from speech_client import AzureSpeechClient
from speech_models import TranscriptionConfig, TranscriptionPayload, TranscriptionJob, TimestampResult
from poll_transcription import poll_transcription

def timestamped_transcript(payload: TranscriptionPayload, config: TranscriptionConfig) -> TimestampResult:
    client = AzureSpeechClient(config)
    
    properties = {
        'wordLevelTimestampsEnabled': True
    }
    
    # Submit the transcription job with word-level timestamps enabled
    submit_response = client.submit_transcription_job(
        display_name=config.job_name or 'timestamped_transcription',
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
        segments = []
        for phrase in completed_job.results.get('recognizedPhrases', []):
            words_data = []
            if 'nBest' in phrase and len(phrase['nBest']) > 0 and 'words' in phrase['nBest'][0]:
                for word_info in phrase['nBest'][0]['words']:
                    offset_seconds = int(word_info['offsetInTicks']) / 10_000_000
                    duration_seconds = int(word_info['durationInTicks']) / 10_000_000
                    words_data.append({
                        "word": word_info['word'],
                        "start_time": str(offset_seconds),
                        "end_time": str(offset_seconds + duration_seconds),
                    })
            
            # For segment level timestamps, use phrase offset and duration
            segment_offset_seconds = int(phrase['offsetInTicks']) / 10_000_000
            segment_duration_seconds = int(phrase['durationInTicks']) / 10_000_000
            segment_text = phrase['nBest'][0]['display']

            segments.append({
                "start_time": str(segment_offset_seconds),
                "end_time": str(segment_offset_seconds + segment_duration_seconds),
                "text": segment_text,
                "words": words_data
            })
        return TimestampResult(segments=segments)
    else:
        raise Exception(f"Timestamped transcription failed or returned no results: {completed_job.status}")
