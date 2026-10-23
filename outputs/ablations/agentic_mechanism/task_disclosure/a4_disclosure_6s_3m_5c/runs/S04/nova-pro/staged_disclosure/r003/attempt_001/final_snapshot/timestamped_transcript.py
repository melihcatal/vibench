import boto3

transcribe = boto3.client('transcribe', region_name='us-west-2')

def get_transcription_job(job_name):
    response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    return response

def get_transcription_results(job_name):
    job = get_transcription_job(job_name)
    if job['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_uri = job['TranscriptionJob']['Transcript']['TranscriptFileUri']
        response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        results = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
        return results
    else:
        return 'Transcription job is not completed.'

def get_timestamps(job_name):
    results = get_transcription_results(job_name)
    if isinstance(results, str) and results.startswith('http'):
        import requests
        response = requests.get(results)
        transcript = response.json()
        timestamps = {}
        for item in transcript['results']['items']:
            if 'start_time' in item and 'end_time' in item:
                timestamps[item['alternatives'][0]['content']] = (item['start_time'], item['end_time'])
        return timestamps
    else:
        return results