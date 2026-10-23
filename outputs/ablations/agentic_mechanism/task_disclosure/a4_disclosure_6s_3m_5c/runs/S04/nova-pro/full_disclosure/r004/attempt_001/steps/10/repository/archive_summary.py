import boto3

def summarize_transcription_results(transcription_job_name):
    transcribe_client = boto3.client('transcribe')
    response = transcribe_client.get_transcription_job(TranscriptionJobName=transcription_job_name)
    transcription_job = response['TranscriptionJob']
    summary = {
        'TranscriptionJobName': transcription_job['TranscriptionJobName'],
        'TranscriptionJobStatus': transcription_job['TranscriptionJobStatus'],
        'LanguageCode': transcription_job['Settings']['LanguageCode'],
        'MediaFormat': transcription_job['Media']['MediaFormat'],
        'MediaFileUri': transcription_job['Media']['MediaFileUri']
    }
    if transcription_job['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_uri = transcription_job['Transcript']['TranscriptFileUri']
        summary['TranscriptUri'] = transcript_uri
    return summary