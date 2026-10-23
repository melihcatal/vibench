from ibm_watson import SpeechToTextV1


def poll_transcription(job_id):
    response = speech_to_text.get_job(job_id)
    return response.get_result()
