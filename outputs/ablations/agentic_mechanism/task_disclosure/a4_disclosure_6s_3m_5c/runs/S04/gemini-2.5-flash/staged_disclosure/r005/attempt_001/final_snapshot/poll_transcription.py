
import time
import requests
import boto3

def poll_transcription_job(job_name, region_name='us-east-1'):
    """
    Polls an AWS Transcribe transcription job and returns the transcript.

    Args:
        job_name (str): The name of the transcription job.
        region_name (str): The AWS region where the job was created.

    Returns:
        str: The transcript if the job is successful, None otherwise.
    """
    transcribe_client = boto3.client('transcribe', region_name=region_name)

    while True:
        response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = response['TranscriptionJob']['TranscriptionJobStatus']

        if job_status == 'COMPLETED':
            transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
            # Fetch the transcript content from the URI
            transcript_content = requests.get(transcript_uri).text
            return transcript_content
        elif job_status == 'FAILED':
            print(f"Transcription job {job_name} failed.")
            return None
        else:
            print(f"Transcription job {job_name} is {job_status}. Waiting...")
            time.sleep(10)  # Wait for 10 seconds before polling again

if __name__ == '__main__':
    # Example usage (replace with your actual job name and region)
    # To run this, you would first need to start a transcription job
    # using transcribe_client.start_transcription_job(...)
    # and then provide the job name here.
    example_job_name = "my-example-transcription-job"
    transcript = poll_transcription_job(example_job_name)

    if transcript:
        print("\nTranscription Complete:")
        print(transcript)
    else:
        print("\nFailed to retrieve transcript.")
