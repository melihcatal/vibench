from google.cloud import speech

def timestamped_transcript(job_id):
    client = speech.SpeechClient()
    operation = client.get_operation(name=job_id)
    if operation.done:
        response = operation.result()
        transcript = response.results[0].alternatives[0].transcript
        timestamps = [
            {
                "word": word.word,
                "start_time": word.start_time.seconds + word.start_time.nanos * 1e-9,
                "end_time": word.end_time.seconds + word.end_time.nanos * 1e-9,
            }
            for word in response.results[0].alternatives[0].words
        ]
        return {
            "status": "COMPLETED",
            "transcript": transcript,
            "timestamps": timestamps,
        }
    else:
        return {"status": "IN_PROGRESS"}