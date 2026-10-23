import boto3

transcribe_client = boto3.client('transcribe')
comprehend_client = boto3.client('comprehend')

def summarize_transcript(transcript):
    response = comprehend_client.start_document_summarization_job(
        Text=transcript,
        DocumentType='PLAIN_TEXT'
    )
    summary_job_id = response['DocumentSummarizationJobProperties']['DocumentSummarizationJobId']
    while True:
        job_status = comprehend_client.get_document_summarization_job(DocumentSummarizationJobId=summary_job_id)['DocumentSummarizationJobProperties']['DocumentSummarizationJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            break
    if job_status == 'COMPLETED':
        summary = comprehend_client.get_document_summarization_job(DocumentSummarizationJobId=summary_job_id)['DocumentSummarizationJobProperties']['OutputDataConfig']['S3Uri']
        return summary
    else:
        return 'Summarization job failed'

# Example usage
transcript = 'This is a sample transcript of a meeting.'
summary = summarize_transcript(transcript)
print(summary)