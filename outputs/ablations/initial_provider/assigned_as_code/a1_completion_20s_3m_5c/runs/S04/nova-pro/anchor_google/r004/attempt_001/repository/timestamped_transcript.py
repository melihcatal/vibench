from google.cloud import speech



def timestamped_transcript(job_id):
    client = speech.SpeechClient()
    operation = client.get_operation(name=job_id)
    if operation.done:
        response = operation.result()
        results = []
        for result in response.results:
            alternatives = result.alternatives
            if alternatives:
                transcript = alternatives[0].transcript
                words = alternatives[0].words
                word_info = []
                for word in words:
                    word_info.append({
                        "word": word.word,
                        "start_time": word.start_time.seconds + word.start_time.nanos * 1e-9,
                        "end_time": word.end_time.seconds + word.end_time.nanos * 1e-9,
                    })
                results.append({
                    "transcript": transcript,
                    "word_info": word_info,
                })
        return {"results": results, "status": "COMPLETED"}
    else:
        return {"status": "IN_PROGRESS"}