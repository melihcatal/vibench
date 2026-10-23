from speech_client import transcribe_client


def poll_transcription(job_name):
    response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
    job_status = response["TranscriptionJob"]["TranscriptionJobStatus"]
    if job_status in ["COMPLETED", "FAILED"]:
        return response
    else:
        return None
