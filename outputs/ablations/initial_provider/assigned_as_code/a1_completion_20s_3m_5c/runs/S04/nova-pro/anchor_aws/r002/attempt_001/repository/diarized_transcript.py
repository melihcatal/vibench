import boto3

from speech_client import get_speech_client


def diarized_transcript(job_id, config=None):
    client = get_speech_client(config)
    response = client.get_transcription_job(TranscriptionJobName=job_id)
    job = response['TranscriptionJob']
    if job['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_uri = job['Transcript']['TranscriptFileUri']
        transcript_response = client.get_object(Bucket=config['bucket'], Key=transcript_uri.split('/')[-1])
        transcript_content = transcript_response['Body'].read().decode('utf-8')
        diarization_response = client.start_speaker_diarization_job(
            SpeakerDiarizationJobName=f"diarization-{uuid.uuid4().hex}",
            LanguageCode=job['LanguageCode'],
            Media={'MediaFileUri': transcript_uri},
            NumberOfSpeakers=2,
        )
        return {
            'job_id': diarization_response['SpeakerDiarizationJob']['SpeakerDiarizationJobName'],
            'status': 'SUBMITTED',
        }
    else:
        return {'status': 'PENDING'}