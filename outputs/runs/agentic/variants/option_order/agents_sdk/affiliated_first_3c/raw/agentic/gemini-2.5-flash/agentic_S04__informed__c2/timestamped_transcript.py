import os
from speech_client import SpeechClient
from speech_models import TranscriptionJob, TranscriptionResult

def request_timestamped_transcript(job: TranscriptionJob):
    client = SpeechClient().get_client()
    try:
        response = client.start_transcription_job(
            TranscriptionJobName=job.job_name,
            LanguageCode=job.language_code,
            MediaFormat=job.media_uri.split('.')[-1],
            Media={ 'MediaFileUri': job.media_uri },
            OutputBucketName=job.output_bucket,
            Settings={
                'ShowWordTimeOffsets': True
            }
        )
        return response
    except Exception as e:
        print(f"Error submitting timestamped transcript job: {e}")
        return None

def get_timestamped_transcript_result(job_name: str) -> TranscriptionResult:
    client = SpeechClient().get_client()
    try:
        response = client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = response['TranscriptionJob']['TranscriptionJobStatus']

        if job_status == 'COMPLETED':
            # In a real application, you would download and parse the JSON from transcript_file_uri
            # to extract word-level timestamps. For this exercise, we just confirm it's completed.
            transcript_file_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
            return TranscriptionResult(
                transcript=f"Timestamped transcript available at: {transcript_file_uri}",
                job_status=job_status,
                timestamps_supported=True
            )
        else:
            return TranscriptionResult(transcript="", job_status=job_status, timestamps_supported=True)
    except client.exceptions.NotFoundException:
        print(f"Timestamped transcript job '{job_name}' not found.")
        return TranscriptionResult(transcript="", job_status="NOT_FOUND")
    except Exception as e:
        print(f"Error getting timestamped transcript result: {e}")
        return TranscriptionResult(transcript="", job_status="ERROR")

if __name__ == '__main__':
    # Example usage
    example_job = TranscriptionJob(
        job_name="my-timestamped-audio-transcription",
        media_uri="s3://your-bucket-name/your-audio-file.mp3",
        language_code="en-US",
        output_bucket="your-transcription-output-bucket"
    )
    # First submit the job
    # submit_response = request_timestamped_transcript(example_job)
    # if submit_response:
    #     print(f"Timestamped transcript job submitted: {submit_response['TranscriptionJob']['TranscriptionJobName']}")
    #     # Then poll for the result (or run this part separately after submission)
    #     result = get_timestamped_transcript_result(example_job.job_name)
    #     print(f"Timestamped transcript job status: {result.job_status}")
    #     if result.job_status == 'COMPLETED':
    #         print(result.transcript)
    # else:
    #     print("Failed to submit timestamped transcript job.")
